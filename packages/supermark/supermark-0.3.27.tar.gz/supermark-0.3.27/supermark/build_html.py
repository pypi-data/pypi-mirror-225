from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Dict, List, Sequence, Set, TYPE_CHECKING

from rich.progress import BarColumn, Progress

from .breadcrumbs import Breadcrumbs
from .chunks import Builder, Chunk, MarkdownChunk, YAMLDataChunk
from .pagemap import Folder
from .report import Report
from .utils import add_notnone, get_relative_path, reverse_path, write_file
from .write_html import div, main_and_aside

if TYPE_CHECKING:
    from .base import Extension


class HTMLBuilder(Builder):
    def __init__(
        self,
        input_path: Path,
        output_path: Path,
        base_path: Path,
        template_file: Path,
        report: Report,
        rebuild_all_pages: bool = True,
        abort_draft: bool = True,
        verbose: bool = False,
        reformat: bool = False,
    ) -> None:
        super().__init__(
            input_path,
            output_path,
            base_path,
            template_file,
            report,
            rebuild_all_pages,
            abort_draft,
            verbose,
            reformat,
        )
        breadcrumbs_path = input_path / Path("breadcrumbs.txt")
        if breadcrumbs_path.exists():
            self.breadcrumbs: Breadcrumbs = Breadcrumbs(self.report, breadcrumbs_path)
            self.report.info(f"Breadcrumbs exist in {breadcrumbs_path}")
        else:
            # old format
            breadcrumbs_path = input_path / Path("breadcrumbs.yaml")
            if breadcrumbs_path.exists():
                self.breadcrumbs: Breadcrumbs = Breadcrumbs(
                    self.report, breadcrumbs_path
                )
                self.report.info(f"Breadcrumbs exist in {breadcrumbs_path}")
            else:
                self.report.info(
                    f"Looking for breadcrumbs file in {breadcrumbs_path}, but it does not exist."
                )

    def _transform_page_to_html(
        self,
        chunks: Sequence[Chunk],
        template: str,
        source_file_path: Path,
        target_file_path: Path,
        report: Report,
        css: str,
        js: str,
    ) -> str:
        for tag in ["content", "css", "js", "rel_path"]:
            if "{" + tag + "}" not in template:
                self.report.warning(
                    "The template does not contain insertion tag {" + tag + "}"
                )
        try:
            return template.format_map(
                {
                    "content": self._main_html_stream_new(
                        chunks, source_file_path, target_file_path
                    ),
                    "css": css,
                    "js": js,
                    "rel_path": reverse_path(self.input_path, source_file_path),
                    "page_source": source_file_path.relative_to(self.input_path),
                }
            )
        except KeyError as e:
            report.error(f"The template contains an unknown key {str(e)}")
            return ""

    def _main_html_stream(
        self,
        chunks: Sequence[Chunk],
        source_file_path: Path,
        target_file_path: Path,
    ) -> str:
        content: List[str] = []
        content.append('<div class="page">')
        content.append('    <section class="content">')

        if self.breadcrumbs.has_breadcrumbs(source_file_path):
            content.append(self.breadcrumbs.get_html(source_file_path, self))

        first_chunk_written = False
        for chunk in chunks:
            if (
                "status" in chunk.page_variables
                and self.abort_draft
                and chunk.page_variables["status"] == "draft"
            ):
                content.append("<mark>This site is under construction.</mark>")
                break
            if isinstance(chunk, YAMLDataChunk):
                pass
            elif not chunk.is_ok():
                print("chunk not ok")
            elif isinstance(chunk, MarkdownChunk):
                if chunk.is_section and first_chunk_written:
                    # open a new section
                    content.append("    </section>")
                    content.append('    <section class="content">')
                # TODO maybe we want to put the anchor element to the top?
                for aside in chunk.asides:
                    add_notnone(
                        div(aside.to_html(self, target_file_path), ["chunk"]), content
                    )
                add_notnone(
                    div(chunk.to_html(self, target_file_path), ["chunk"]), content
                )
                first_chunk_written = True
            else:
                # add_notnone(chunk.to_html(self, target_file_path), content)
                for aside in chunk.asides:
                    add_notnone(
                        div(aside.to_html(self, target_file_path), ["chunk"]), content
                    )
                add_notnone(
                    div(chunk.to_html(self, target_file_path), ["chunk"]), content
                )
                first_chunk_written = True

        content.append("    </section>")
        content.append("</div>")
        return "\n".join(content)

    def _group_chunks_into_sections(
        self,
        chunks: Sequence[Chunk],
    ) -> Sequence[Sequence[Chunk]]:
        result: List[List[Chunk]] = []
        current_section: List[Chunk] = []
        keep_with_next: bool = False
        for chunk in chunks:
            if isinstance(chunk, YAMLDataChunk):
                pass
            elif not chunk.is_ok():
                pass
            elif (
                isinstance(chunk, MarkdownChunk)
                and (chunk.is_section and not keep_with_next)
                and current_section
            ):
                # Append the current section to the result and start a new section
                result.append(current_section)
                current_section = [chunk]
            else:
                # Append the chunk to the current section
                current_section.append(chunk)
            keep_with_next = chunk.html_keep_with_next()

        # Append the last section if it's not empty
        if current_section:
            result.append(current_section)
        return result

    def _main_html_stream_new(
        self,
        chunks: Sequence[Chunk],
        source_file_path: Path,
        target_file_path: Path,
    ) -> str:
        content: List[str] = []

        margin_top = "mt-5"
        if self.breadcrumbs.has_breadcrumbs(source_file_path):
            content.append(self.breadcrumbs.get_html(source_file_path, self))
            margin_top = "mt-2"

        sections = self._group_chunks_into_sections(chunks)
        for section in sections:
            content.append(f'<section class="{margin_top} mb-5 py-3">')
            for chunk in section:
                content.append(
                    main_and_aside(
                        chunk.to_html(self, target_file_path),
                        [
                            aside.to_html(self, target_file_path)
                            for aside in chunk.asides
                        ],
                    )
                )
            content.append("</section>")
        return "\n".join(content)

    def _create_target(
        self,
        source_file_path: Path,
        target_file_path: Path,
        template_file_path: Path,
        overwrite: bool,
    ) -> bool:
        if not target_file_path.is_file():
            return True
        if overwrite:
            return True
        if not template_file_path.is_file():
            return target_file_path.stat().st_mtime < source_file_path.stat().st_mtime
        else:
            return (
                target_file_path.stat().st_mtime < source_file_path.stat().st_mtime
            ) or (target_file_path.stat().st_mtime < template_file_path.stat().st_mtime)

    def _process_file(
        self,
        source_file_path: Path,
        target_file_path: Path,
        template: str,
    ):
        extensions_used: Set[Extension] = set()
        chunks = self.parse_file(source_file_path, extensions_used)
        if not chunks:
            # TODO warn that the page is empty, and therefore nothing is written
            return

        html = self._transform_page_to_html(
            chunks,
            template,
            source_file_path,
            target_file_path,
            self.report,
            self.core.get_css(extensions_used),
            self.core.get_js(extensions_used),
        )
        write_file(html, target_file_path, self.report)
        self.report.info("Translated", path=target_file_path)

    def _default_html_template(self) -> str:
        html: List[str] = []
        html.append('<head><title></title><style type="text/css">{css}</style></head>')
        html.append("<body>")
        html.append("{content}")
        html.append("</body>")
        html.append("</html>")
        return "\n".join(html)

    def _load_html_template(self, template_path: Path, report: Report) -> str:
        try:
            with open(
                template_path, encoding="utf-8", errors="surrogateescape"
            ) as templatefile:
                template = templatefile.read()
                self.report.info(f"Loading template {template_path}.")
                return template
        except FileNotFoundError:
            self.report.warning(
                "Template file missing. Expected at {}. Using default template.".format(
                    template_path
                )
            )
            return self._default_html_template()

    def get_target_file(self, source_file_path: Path) -> Path:
        return (
            self.output_path
            / source_file_path.relative_to(self.input_path).parent
            / (source_file_path.stem + ".html")
        )

    def build(
        self,
    ) -> None:
        template = self._load_html_template(self.template_file, self.report)
        jobs: List[Dict[str, Any]] = []
        files = list(
            self.input_path.glob(
                "**/*.md",
            )
        )
        self.output_path.mkdir(exist_ok=True, parents=True)
        for source_file_path in files:
            target_file_path = self.get_target_file(source_file_path)
            if self._create_target(
                source_file_path,
                target_file_path,
                self.template_file,
                self.rebuild_all_pages,
            ):
                target_file_path.parent.mkdir(exist_ok=True, parents=True)
                jobs.append(
                    {
                        "source_file_path": source_file_path,
                        "target_file_path": target_file_path,
                        "template": template,
                        "abort_draft": self.abort_draft,
                    }
                )
        if len(files) == 0:
            self.report.conclude(
                "No source files (*.md) detected. Searched in {}".format(
                    self.input_path
                )
            )
            return
        elif len(jobs) == 0:
            self.report.conclude(
                "No changed files detected. To re-build all unchanged files, use the [bold]--all[/bold] option."
            )
            return
        if len(jobs) == 1:
            self.report.info("Using single thread.")
            with Progress(transient=True) as progress:
                progress.add_task("[orange]Building 1 page", start=False)
                self._process_file(
                    jobs[0]["source_file_path"],
                    jobs[0]["target_file_path"],
                    jobs[0]["template"],
                )
        else:
            with ThreadPoolExecutor() as e:
                self.report.info("Using threadpool.")
                with Progress(
                    "[progress.description]{task.description}",
                    BarColumn(),
                    "[progress.percentage]{task.percentage:>3.0f}%",
                    transient=True,
                ) as progress:
                    task = progress.add_task(
                        f"[orange]Building {len(jobs)} pages",
                        total=len(jobs),
                    )
                    futures = []
                    for job in jobs:
                        future = e.submit(
                            self._process_file,
                            job["source_file_path"],
                            job["target_file_path"],
                            job["template"],
                        )
                        future.add_done_callback(
                            lambda p: progress.update(task, advance=1.0)
                        )
                        futures.append(future)
                    for future in futures:
                        future.result()

    def _get_html_folder(
        self, folder: Folder, target_file_path: Path, html: List[str], indent: str = ""
    ):
        if folder.title is not None:
            if folder.index_path is not None:
                target = get_relative_path(
                    target_file_path, self.get_target_file(folder.index_path)
                )
                html.append(indent + f'<a href="{target}">{folder.title}</a>')
            else:
                html.append(indent + f'<a href="#">{folder.title}</a>')
        html.append(indent + "<ul>")
        for group in folder.page_groups.values():
            html.append(indent + f"<li>{group.page_group_id.capitalize()}<ul>")
            for page in group.pages.values():
                target = get_relative_path(
                    target_file_path, self.get_target_file(page.path)
                )
                html.append(
                    indent + f'<li><a href="{target}">{page.get_title()}</a></li>'
                )
            html.append(indent + "</ul></li>")
        for page in folder.pages.values():
            target = get_relative_path(
                target_file_path, self.get_target_file(page.path)
            )
            html.append(indent + f'<li><a href="{target}">{page.get_title()}</a></li>')

        for f in folder.folders:
            if f.contains_pages():
                html.append(indent + "<li>")
                self._get_html_folder(f, target_file_path, html, indent + "    ")
                html.append(indent + "</li>")
        html.append(indent + "</ul>")
