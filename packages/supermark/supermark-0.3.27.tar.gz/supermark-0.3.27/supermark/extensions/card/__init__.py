from pathlib import Path
from typing import Any, Dict, List, Optional

from ... import (
    Builder,
    Chunk,
    RawChunk,
    YAMLChunk,
    YamlExtension,
    YAMLGroupChunk,
    get_placeholder_uri_str,
)


class CardExtension(YamlExtension):
    def __init__(self):
        super().__init__(type="card", chunk_class=Card)


class CardGroupExtension(YamlExtension):
    def __init__(self):
        super().__init__(type="cards", chunk_class=CardGroup)


class CardGroup(YAMLGroupChunk):
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
            required=None,
            optional=["columns"],
        )
        self.chunks: List[Chunk] = []

    def accepts(self, chunk: Chunk) -> bool:
        return isinstance(chunk, Card)

    def is_group(self) -> bool:
        return True

    def add_chunk(self, chunk: Chunk):
        self.chunks.append(chunk)

    def finish(self):
        ...

    def to_html(self, builder: Builder, target_file_path: Path) -> Optional[str]:
        html: List[str] = []
        columns = self.dictionary["columns"] if "columns" in self.dictionary else 2

        if columns < 1:  # or columns > 3:
            self.warning("Columns for cards set to 2")
            columns = 2

        html.append(f'<div class="row row-cols-1 row-cols-md-{columns} g-4">')
        for chunk in self.chunks:
            c = chunk.to_html(builder=builder, target_file_path=target_file_path)
            if c:
                html.append('<div class="col">')
                html.append(c)
                html.append("</div>")
        html.append("</div>")
        return "\n".join(html)


class Card(YAMLChunk):
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
            required=None,
            optional=[
                "link",
                "title",
                "kind",
                "name",
                "detail",
                "image",
                "email",
                "text",
                "link_title",
            ],
        )

    def is_groupable(self) -> bool:
        return True

    def get_group(self) -> Any:
        return CardGroup(self.raw_chunk, {"type": "cards"}, self.page_variables)

    def _placeholder(self, src: str) -> str:
        if src.startswith("_placeholder"):
            return get_placeholder_uri(80, 80)
        return src

    def _create_card_person(
        self,
        name: str,
        email: str,
        detail: str,
        img: str,
        html: List[str],
        builder: Builder,
    ):
        html.append(
            '<div class="card border-0 person-card h-100" style="max-width: 540px;">'
        )
        html.append('    <div class="row g-0">')
        html.append('        <div class="col-md-3">')
        html.append(
            f'            <img src="{get_placeholder_uri_str(img)}" class="img-fluid" alt="Photo of {name}">'
        )
        html.append("        </div>")
        html.append('        <div class="col-md-9">')
        html.append(
            '            <div class="card-body" style="padding: 0px 0px 0px 5px">'
        )
        html.append(f'                <div class="person-card-name">{name}</div>')
        html.append(f'                <div class="person-card-detail">{detail}</div>')
        html.append(
            f'                <a class="person-card-email stretched-link" href="mailto:{email}">{email}</a>'
        )
        html.append("            </div>")
        html.append("        </div>")
        html.append("        </div>")
        html.append("</div>")

        file_path = (self.raw_chunk.path.parent / Path(img)).resolve()
        if file_path.exists():
            builder.copy_resource(self.raw_chunk, file_path)

    def _create_card_arrow(self, title: str, href: str, html: List[str]):
        html.append('<div class="card text-end shadow-sm h-100">')
        html.append('<div class="card-body">')
        html.append(f'    <h5 class="card-title">{title}</h5>')
        html.append(f'    <a href="{href}" class="stretched-link">')
        html.append('    <i class="bi bi-arrow-right-circle fs-1"></i>')
        html.append("    </a>")
        html.append("</div>")
        html.append("</div>")

    def _create_card_text(
        self,
        title: str,
        text: str,
        link: str,
        html: List[str],
        link_title: Optional[str] = None,
    ):
        html.append('    <div class="card shadow-sm h-100">')
        html.append('    <div class="card-body">')
        html.append(f'        <h5 class="card-title">{title}</h5>')
        html.append(f'        <p class="card-text">{text}</p>')
        if link_title is None:
            html.append(f'        <a href="{link}" class="stretched-link"></a>')
        else:
            html.append("<ul>")
            html.append(
                f'    <li><a href="{link}" class="stretched-link">{link_title}</a></li>'
            )
            html.append("</ul>")
        html.append("    </div>")
        html.append("    </div>")

    def _create_post_yaml_card(
        self, post_yaml: str, title: Optional[str], html: List[str], builder: Builder
    ):
        html.append('<div class="card h-100"">')
        html.append('<div class="card-body">')
        if title is not None and len(title) > 0:
            html.append(f'<h6 class="card-title">{title}</h6>')
        html.append(builder.convert(post_yaml, "html"))
        html.append("</div>")
        html.append("</div>")

    def to_html(self, builder: Builder, target_file_path: Path):
        html: List[str] = []

        link = self.dictionary["link"] if "link" in self.dictionary else ""
        link_title = (
            self.dictionary["link_title"] if "link_title" in self.dictionary else None
        )
        type = self.dictionary["type"]
        name = self.dictionary.get("name", "")
        email = self.dictionary.get("email", "")
        detail = self.dictionary.get("detail", "")
        title = self.dictionary.get("title", "")
        image = self.dictionary.get("image", "")
        text = self.dictionary.get("text", "")

        if type == "card/person":
            self._create_card_person(name, email, detail, image, html, builder)
        elif type == "card/arrow":
            self._create_card_arrow(title, link, html)
        elif type == "card/text":
            self._create_card_text(title, text, link, html, link_title)
        elif type == "card" and self.get_post_yaml() is not None:
            self._create_post_yaml_card(self.get_post_yaml(), title, html, builder)

        return "\n".join(html)
