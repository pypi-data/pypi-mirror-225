from pathlib import Path
from typing import Any, Dict, Optional, List
from shutil import copyfile

from ... import (
    Builder,
    RawChunk,
    RawChunkType,
    YAMLChunk,
    HTMLChunk,
    YamlExtension,
    is_placeholder,
    get_placeholder_uri_str,
)


class FigureExtension(YamlExtension):
    def __init__(self):
        super().__init__(type="figure", chunk_class=Figure)


class Figure(YAMLChunk):
    def __init__(
        self,
        raw_chunk: RawChunk,
        dictionary: Dict[str, Any],
        page_variables: Dict[str, Any],
    ):
        super().__init__(
            raw_chunk,
            dictionary,
            page_variables,
            required=["source"],
            optional=["caption", "link"],
            # TODO add figure credits
        )
        source = dictionary["source"]
        self.placeholder = None
        self.file_path = None
        self.name = None
        # TODO base the name on a hash ID of the raw chunk?
        if source.startswith("http://") or source.startswith("https://"):
            self.tell(
                f"Refer to remote figure: {source}",
                level=self.WARNING,
            )
            self.name = source
        elif is_placeholder(source):
            self.placeholder = source
            self.name = source
        else:
            self.file_path = (raw_chunk.path.parent / Path(source)).resolve()
            self.name = source
        # add caption as aside element
        if "caption" in self.dictionary:
            # self.asides.insert(0, MarkdownChunk())
            self.asides.insert(
                0,
                HTMLChunk.create_derived_chunk(
                    f'<figcaption class="figure-caption">{self.dictionary["caption"]}</figcaption>',
                    self.raw_chunk,
                ),
            )

    def _get_target_relative_path(
        self, builder: Builder, target_file_path: Path
    ) -> str:
        # TODO this can be simplified
        path = self.file_path.relative_to(builder.input_path)
        target = builder.output_path / path
        return str(target.relative_to(target_file_path.parent))

    def to_html(self, builder: Builder, target_file_path: Path):
        if self.file_path is not None:
            if not self.file_path.exists():
                if builder.core.image_file_locator is not None:
                    # try to find the file in another place
                    other_file = builder.core.image_file_locator.lookup(self.file_path)
                    if other_file is not None:
                        target = (
                            self.raw_chunk.path.parent / "figures" / self.file_path.name
                        )
                        if not target.exists():
                            target.parent.mkdir(exist_ok=True)
                            self.tell(
                                f"Found matching file {other_file} and copied it to {target}.",
                                level=self.WARNING,
                            )
                            copyfile(other_file, target)
                            # TODO should we rewrite the source file path in the original chunk?
            if self.file_path.exists():
                builder.copy_resource(self.raw_chunk, self.file_path)
            else:
                self.tell(
                    f"Figure file {str(self.file_path)} does not exist.",
                    level=self.WARNING,
                )

        alt = self.dictionary.get("caption", "")
        src = None
        if self.file_path is not None:
            src = self._get_target_relative_path(builder, target_file_path)
        elif "link" in self.dictionary:
            src = self.dictionary["link"]
        elif self.placeholder:
            src = get_placeholder_uri_str(self.placeholder)
        html: List[str] = []
        html.append('<figure class="figure">')
        if "link" in self.dictionary:
            html.append(f'  <a href="{self.dictionary["link"]}">')
        html.append(
            f'    <img src="{src}" class="figure-img img-fluid rounded" alt="{alt}">'
        )
        if "link" in self.dictionary:
            html.append("  </a>")
        # if "caption" in self.dictionary:
        #     html.append(
        #         f'  <figcaption class="figure-caption">{self.dictionary["caption"]}</figcaption>'
        #     )
        html.append("</figure>")
        return "\n".join(html)

    def to_html_old(self, builder: Builder, target_file_path: Path):
        if self.file_path is not None:
            builder.copy_resource(self.raw_chunk, self.file_path)
        html: List[str] = []
        html.append('<div class="figure">')
        if "caption" in self.dictionary:
            if "link" in self.dictionary:
                html.append(
                    '<a href="{}"><img src="{}" alt="{}" width="100%"/></a>'.format(
                        self.dictionary["link"],
                        self._get_target_relative_path(builder, target_file_path),
                        self.dictionary["caption"],
                    )
                )
            elif self.file_path is not None:
                html.append(
                    '<img src="{}" alt="{}" width="100%"/>'.format(
                        self._get_target_relative_path(builder, target_file_path),
                        self.dictionary["caption"],
                    )
                )
            elif self.placeholder:
                html.append(
                    f'<img src="{get_placeholder_uri_str(self.placeholder)}" alt="{self.dictionary["caption"]}" width="100%"/>'
                )
            html.append(f'<span name="{self.name}">&nbsp;</span>')
            html_caption: str = builder.convert(
                self.dictionary["caption"], target_format="html", source_format="md"
            )
            html.append(
                '<aside name="{}"><p>{}</p></aside>'.format(
                    self.name,
                    html_caption,
                )
            )
        else:
            if "link" in self.dictionary:
                html.append(
                    '<a href="{}"><img src="{}" width="100%"/></a>'.format(
                        self.dictionary["link"],
                        self._get_target_relative_path(builder, target_file_path),
                    )
                )
            elif self.file_path is not None:
                html.append(
                    '<img src="{}" alt="" width="100%"/>'.format(
                        self._get_target_relative_path(builder, target_file_path),
                    )
                )
            elif self.placeholder is not None:
                html.append(
                    f'<img src="{get_placeholder_uri_str(self.placeholder)}" alt="{self.dictionary["caption"]}" width="100%"/>'
                )
        html.append("</div>")
        return "\n".join(html)

    def to_latex(self, builder: Builder, target_file_path: Path) -> Optional[str]:
        s: List[str] = []
        s.append("\\begin{figure}[htbp]")
        # s.append('\\begin{center}')
        # file = '../' + self.dictionary['source']
        figure_file = self.raw_chunk.parent_path / self._get_target_relative_path(
            builder, target_file_path
        )
        # print(figure_file.suffix)
        if figure_file.suffix == ".gif":
            self.tell(
                "Figure file {} in gif format is not compatible with LaTeX.".format(
                    self.file_path
                ),
                level=self.WARNING,
            )
            return None
        if figure_file.suffix == ".svg":
            # file = Path(file)
            target_path = self.get_dir_cached() / f"{figure_file.stem}.pdf"
            if not target_path.exists():
                import cairosvg

                # file = self.raw_chunk.parent_path / self.dictionary['source']
                cairosvg.svg2pdf(url=str(figure_file), write_to=str(target_path))
            # s.append('\\includegraphics[width=\\linewidth]{{{}}}%'.format(target_path))
            figure_file = target_path
        figure_file = figure_file.relative_to(builder.output_file.parent)
        # print('figure_file: {}'.format(figure_file))
        s.append(f"\\includegraphics[width=\\linewidth]{{{figure_file}}}%")
        if "caption" in self.dictionary:
            s.append(
                "\\caption{{{}}}".format(
                    builder.convert(
                        self.dictionary["caption"],
                        target_format="latex",
                        source_format="md",
                    )
                )
            )
        s.append("\\label{default}")
        # s.append('\\end{center}')
        s.append("\\end{figure}")
        return "\n".join(s)
