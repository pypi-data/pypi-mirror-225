from pathlib import Path
from typing import Any, Dict, List

from ... import Builder, RawChunk, YAMLChunk, YamlExtension, get_icon


class NavExtension(YamlExtension):
    def __init__(self):
        super().__init__(type="nav", chunk_class=Nav)


class Nav(YAMLChunk):
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
            required=[],
            optional=["prev", "next", "up"],
        )

    def _get_icon(self, link: str) -> str:
        if link == "prev":
            return get_icon("arrow-left-short", size="16")
        elif link == "next":
            return get_icon("arrow-right-short", size="16")
        return ""

    def html_keep_with_next(self) -> bool:
        return True

    def to_html(self, builder: Builder, target_file_path: Path):
        html: List[str] = []
        html.append('<nav class="d-flex justify-content-between">')
        if "prev" in self.dictionary:
            html.append(
                '<a type="button" href="{}" class="page-link rounded">'.format(
                    self.dictionary["prev"][1]
                )
            )
            html.append(get_icon("arrow-left-short", size="16"))
            html.append(f"{self.dictionary['prev'][0]}")
            html.append("</a>")
        else:
            html.append("<div></div>")
        if "up" in self.dictionary:
            html.append(
                '<a type="button" href="{}" class="page-link rounded">'.format(
                    self.dictionary["up"][1]
                )
            )
            html.append(f"{self.dictionary['up'][0]}")
            html.append("</a>")
        else:
            html.append("<div></div>")
        if "next" in self.dictionary:
            html.append(
                f'<a type="button" href="{self.dictionary["next"][1]}" class="page-link rounded">'
            )
            html.append(f"{self.dictionary['next'][0]}")
            html.append(get_icon("arrow-right-short", size="16"))
            html.append("</a>")
        else:
            html.append("<div></div>")
        html.append("</nav>")
        return "\n".join(html)
