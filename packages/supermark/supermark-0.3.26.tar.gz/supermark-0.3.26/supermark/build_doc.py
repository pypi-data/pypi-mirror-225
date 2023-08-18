from pathlib import Path
from shutil import copy
from typing import List, Sequence, Set

import supermark.doc

from .base import Extension
from .chunks import Builder, Chunk
from .examples_yaml import YAMLExamples
from .report import Report
from .utils import write_file, none_str
from .write_md import nav_link_back
from .write_html import HTMLTable, html_link

DOC_FOLDER = "supermark"


class DocBuilder(Builder):
    def __init__(
        self,
        input_path: Path,
        output_path: Path,
        base_path: Path,
        template_file: Path,
        report: Report,
        verbose: bool = False,
    ) -> None:
        super().__init__(
            input_path,
            output_path,
            base_path,
            template_file,
            report,
            verbose,
        )
        self.target_folder = input_path / DOC_FOLDER

    def find_used_extensions(self) -> Set[Extension]:
        files = list(
            self.input_path.glob(
                "**/*.md",
            )
        )
        files = [file for file in files if not file.match(f"{DOC_FOLDER}/**")]
        extensions_used: Set[Extension] = set()
        for source_file_path in files:
            _ = self.parse_file(source_file_path, extensions_used)
        return extensions_used

    def build(
        self,
    ) -> None:
        self.target_folder.mkdir(exist_ok=True)
        self.copy_docs()
        # extensions_used = self.find_used_extensions()

        # Overview page
        md: List[str] = []
        nav_link_back("Documentation", "index.html", md)
        md.append("# Extensions")
        md.append(self.build_all_extensions_table_2().get_html())
        md.append("\n\n")
        # for used in [True, False]:
        #     if used:
        #         md.append("### Extensions used in this Site")
        #     else:
        #         md.append("### Other Extensions")
        #     md.append("<ul>")
        #     # for folder in sorted(folders):
        #     folders: set[Path] = set()
        #     for extension in self.core.get_all_extensions():
        #         # Extensions can show up several times, but folder is unique
        #         folder = extension.folder
        #         if folder in folders:
        #             continue
        #         folders.add(extension.folder)
        #         is_used = extension in extensions_used
        #         if is_used != used:
        #             continue
        #         x = str(folder.name)
        #         doc = extension.get_doc_summary()
        #         if doc is None:
        #             doc = ""
        #         md.append(f'<li><a href="{x}.html">{x}</a> {doc}</li>')
        #     md.append("</ul>\n\n\n\n")
        write_file("\n".join(md), self.target_folder / "extensions.md", self.report)

        # Page for each extension
        for extension_package in self.core.extension_packages.values():
            mdx: List[str] = []
            nav_link_back("All extensions", "extensions.html", mdx)

            mdx.append(f"\n\n# Extension {extension_package.folder.name}\n")
            doc = extension_package.get_doc()
            if doc is not None and doc.exists():
                with open(doc, encoding="utf-8") as file:
                    lines = file.readlines()
                    mdx.append("".join(lines))

            # Table for each extension
            for extension in sorted(
                extension_package.extensions, key=lambda e: e.get_name()
            ):
                mdx.append(extension.get_doc_table().get_html())

            # for now, all examples:
            example_chunks = self._load_example_chunks(extension)
            ye = YAMLExamples(example_chunks)
            ye.write_doc(mdx)
            for index, example in enumerate(extension.get_examples()):
                if example.exists():
                    self._build_example(extension, example, index, mdx)

            write_file(
                "\n".join(mdx),
                self.target_folder / f"{extension_package.folder.name}.md",
                self.report,
            )

    def copy_docs(self):
        for file in Path(supermark.doc.__file__).parent.glob("*.md"):
            copy(file, self.target_folder)

    def _load_example_chunks(
        self,
        extension: Extension,
    ) -> Sequence[Chunk]:
        example_chunks: List[Chunk] = []
        for example in extension.get_examples():
            chunks = self.core.parse_file(example)
            if chunks is not None:
                for c in chunks:
                    example_chunks.append(c)
        return example_chunks

    def _build_example(
        self, extension: Extension, example: Path, index: int, md: List[str]
    ):
        md.append(f"\n\n# Example {index+1}\n")
        code: str = ""
        # include example directly, to show the result
        with open(example, encoding="utf-8") as file:
            code = "".join(file.readlines())
        md.append(code)
        md.append("\n\n\n")
        md.append("\n\n## Source Code\n")
        # include code of the example
        md.append(f"```{self._guess_code_language(code)}")
        md.append(code)
        md.append("```")
        md.append("\n\n\n")

    def _guess_code_language(self, code: str) -> str:
        if code.startswith("---"):
            return "yaml"
        return ""

    def build_all_extensions_table(self) -> HTMLTable:
        table: HTMLTable = HTMLTable(css_class="table")
        for extension in self.core.get_all_extensions():
            table.add_row(
                extension.get_name(),
                str(type(extension).__name__),
                extension.package.folder.name,
                extension.extension_point.name,
            )
            table.flush_row()
        table.flush_row_group()
        return table

    def build_all_extensions_table_2(self) -> HTMLTable:
        table: HTMLTable = HTMLTable(css_class="table")
        table.add_cell("Pack", header=True)
        table.add_cell("Doc", header=True)
        table.add_cell("Extensions", header=True)
        table.flush_row()
        for extension_package in sorted(
            filter(lambda ep: not ep.is_alpha(), self.core.extension_packages.values()),
            key=lambda e: e.folder.name,
        ):
            extensions = extension_package.extensions
            name = extension_package.folder.name
            # <a href="{x}.html">{x}</a>
            table.add_cell(html_link(f"{name}.html", name), rowspan=len(extensions))
            table.add_cell(
                none_str(extension_package.get_doc_summary()), rowspan=len(extensions)
            )

            for extension in extensions:
                table.add_cell(
                    extension.get_name(),
                )
                table.flush_row()
        table.flush_row_group()
        return table

        #        table.add_row("type", ", ".join(list(self.get_types(type))))
        #        table.add_row("Language", html_link("#", "YAML"))
        #        table.add_row("Required fields", ", ".join(self.get_required(type)))
        #        table.add_row("Optional fields", ", ".join(self.get_optional(type)))
        #        table.add_row("Post-Yaml Section", self.has_post_yaml(type))
        table.flush_row_group()
        return table
