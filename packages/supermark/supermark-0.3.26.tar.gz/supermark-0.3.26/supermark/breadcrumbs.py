from pathlib import Path
import pprint
from rich import print
from rich.tree import Tree
from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .build_html import HTMLBuilder

import yaml
from yaml.scanner import ScannerError

from .report import Report
from .utils import get_relative_path


class Page:
    def __init__(
        self, path: Path, page: str, title: str, children: Optional[List["Page"]] = None
    ):
        self.page = page
        self.page_path = path
        # TODO handle that these are not set
        self.parent = None
        if children:
            self.children = children
            for child in self.children:
                child.parent = self
        else:
            self.children = []

    def __str__(self):
        return self.title

    def print_tree(self, tree: Tree = None, level: int = 0):
        if tree is None:
            tree = Tree(self.title)

        if self.children:
            for child in self.children:
                child_tree = tree.add(child.title)
                child.print_tree(child_tree, level + 1)

        if level == 0:
            print(tree)


class Breadcrumbs:
    def __init__(self, report: Report, path: Path):
        self.pages: Dict[Path, Page] = {}
        self.report = report
        self.path = path
        if path.suffix == ".yaml":
            with open(path) as f:
                try:
                    temp: Any = yaml.safe_load(f)
                    self.roots = self.parse_breadcrumbs(temp, path.parent)
                    if report.verbose:
                        for page in self.roots:
                            page.print_tree()
                    # store in new format
                    x = self.serialize_page_trees()
                    path.with_suffix(".txt").write_text(x)
                except ScannerError as e:
                    self.report.warning(str(e), path)
        else:
            text = path.read_text()
            lines = text.split("\n")
            self.roots = self.deserialize_page_trees(lines)

    def parse_breadcrumbs(self, l: List[Any], path: Path) -> List[Any]:
        """[{page}, [children]]"""
        tchildren = []
        for i in range(len(l)):
            item = l[i]
            if isinstance(item, dict):
                if i < len(l) - 1 and isinstance(l[i + 1], list):
                    children = self.parse_breadcrumbs(l[i + 1], path)
                else:
                    children = None
                title = item["title"] if "title" in item else item["page"]
                page = Page(path, item["page"], title, children=children)
                tchildren.append(page)
                page_path = path / Path(item["page"])
                if not page_path.exists():
                    self.report.warning(
                        f"Page {item['page']} in breadcrumbs does not exist.", self.path
                    )
                self.pages[page_path] = page
        return tchildren

    def serialize_page_trees(self) -> str:
        lines: List[str] = []
        for root in self.roots:
            lines.extend(self.serialize_page_tree(root))
            lines.append("")  # Add an empty line between trees
        # return lines[:-1]  # Remove the last empty line
        return "\n".join(lines)

    def serialize_page_tree(self, root, indent=0) -> List[str]:
        lines: List[str] = []
        prefix = "  " * indent
        lines.append(f"{prefix}{root.page} - {root.title}")
        if root.children:
            for child in root.children:
                lines.extend(self.serialize_page_tree(child, indent + 1))
        return lines

    def deserialize_page_trees(self, lines):
        roots = []
        current_tree_lines = []
        for line in lines:
            if line.strip():
                current_tree_lines.append(line)
            else:
                roots.append(self.deserialize_page_tree(current_tree_lines))
                current_tree_lines = []
        if current_tree_lines:
            roots.append(self.deserialize_page_tree(current_tree_lines))
        return roots

    def deserialize_page_tree(self, lines):
        stack = []
        root = None
        for line in lines:
            indent = int((len(line) - len(line.lstrip(" "))) / 2)
            page, title = line.strip().split(" - ")
            parent = None
            if indent > 0 and len(stack) >= indent:  # Ensure stack length is checked
                parent = stack[
                    indent - 1
                ]  # Get the parent from the stack based on indent
            page_path = self.path.parent / Path(page)
            node = Page(page_path, page, title)
            node.parent = parent
            self.pages[page_path] = node
            if indent == 0 and root is None:  # Only set root once
                root = node
            elif parent:
                parent.children.append(node)
            # Update the stack
            if len(stack) > indent:
                stack = stack[:indent]  # Truncate the stack to the current indent
            stack.append(node)
        return root

    def has_breadcrumbs(self, page: Path) -> bool:
        return page in self.pages

    def get_trail(self, page_path: Path) -> List[Page]:
        if page_path not in self.pages:
            return []
        page = self.pages[page_path]
        trail: List[Page] = []
        trail.append(page)
        while page.parent is not None:
            trail.append(page.parent)
            page = page.parent
        trail.reverse()
        return trail

    def get_html(self, input_page: Path, builder: "HTMLBuilder") -> str:
        html: List[str] = []
        divider = "url(&#34;data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='8' height='8'%3E%3Cpath d='M2.5 0L1 1.5 3.5 4 1 6.5 2.5 8l4-4-4-4z' fill='%236c757d'/%3E%3C/svg%3E&#34;)"
        html.append(
            f'<nav style="--bs-breadcrumb-divider: {divider};" aria-label="breadcrumb">'
        )
        html.append('<ol class="breadcrumb">')
        for page in self.get_trail(input_page):
            if page.page_path == input_page:
                html.append(
                    f'<li class="breadcrumb-item active" aria-current="page">{page.title}</li>'
                )
            else:
                path = get_relative_path(
                    builder.get_target_file(input_page),
                    builder.get_target_file(page.page_path),
                )
                html.append(
                    f'<li class="breadcrumb-item"><a href="{path}">{page.title}</a></li>'
                )
        html.append("</ol>")
        html.append("</nav>")
        return "\n".join(html)


class Page2:
    def __init__(self, path: Path, title: str):
        self.path = path
        self.title = title
        self.children: List[Page2] = []

    def get_list(self) -> List[Any]:
        if len(self.children) > 0:
            children = [x.get_list() for x in self.children]
            return [{"path": self.path, "title": self.title}, children]
        else:
            return [{"path": self.path, "title": self.title}]
