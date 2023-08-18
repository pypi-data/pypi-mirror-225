from typing import List, Optional, Sequence, Union


def html_link(href: str, title: str) -> str:
    return f'<a href="{href}">{title}</a>'


def div(content: str, classes: Optional[Sequence[str]] = None) -> str:
    atts = f' class="{" ".join(classes)}"' if classes else ""
    return f"<div{atts}>{content}</div>"


def aside(content: str, aside_id: str, classes: Optional[Sequence[str]] = None) -> str:
    atts = f' class="{" ".join(classes)}"' if classes else ""
    return f'<span name="{aside_id}"></span><aside name="{aside_id}"{atts}>{content}</aside>'


def main_and_aside(main: str, asides: Optional[Union[str, Sequence[str]]]) -> str:
    s = '<div class="row g-0 my-3">'
    s += '<div class="col-md-8 px-4 chunk">' + main + "</div>"
    if asides is not None:
        s += '<aside class="col-md-4 chunk ps-2">'
        for aside in asides if isinstance(asides, Sequence) else [asides]:
            s += aside
        s += "</aside>"
    s += "</div>"
    return s


class HTMLTable:
    def __init__(
        self, css_class: Optional[str] = None, css_id: Optional[str] = None
    ) -> None:
        self.css_class = css_class
        self.css_id = css_id
        self.rows: List[str] = []
        self.row_groups: List[str] = []
        self.row_under_construction: List[str] = []
        self.row_group_under_construction: List[str] = []

    def add_row(self, *cells: str) -> None:
        self.rows.append("<td>" + "</td><td>".join(cells) + "</td>")

    def add_cell(
        self,
        cell_content: str,
        rowspan: int = 1,
        colspan: int = 1,
        header: bool = False,
        css_class: Optional[str] = None,
    ) -> None:
        cell = "<th " if header else "<td "
        if rowspan > 1:
            cell = cell + f'rowspan="{rowspan}" '
        if colspan > 1:
            cell = cell + f'colspan="{colspan}" '
        if css_class is not None:
            cell = cell + f'class="{css_class}" '
        cell = cell + ">"
        cell = cell + cell_content + ("</th>" if header else "</td>")
        self.row_under_construction.append(cell)

    def flush_row(self) -> None:
        self.rows.append("<tr>" + "\n".join(self.row_under_construction) + "</tr>")
        self.row_under_construction = []

    def flush_row_group(self) -> None:
        self.row_groups.append("<tbody>" + "\n".join(self.rows) + "</tbody>")
        self.rows = []

    def get_html(self) -> str:
        return (
            "<table"
            + ("" if self.css_class is None else f' class="{self.css_class}"')
            + ("" if self.css_id is None else f' id="{self.css_id}"')
            + ">"
            + "\n".join(self.row_groups)
            + "</table>"
        )
