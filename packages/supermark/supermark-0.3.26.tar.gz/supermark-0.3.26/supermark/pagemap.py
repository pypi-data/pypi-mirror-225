from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Union

from .chunks import MarkdownChunk
from .core import Core
from .report import Report


@dataclass
class Folder:
    path: Path
    is_root: bool = False
    index_path: Optional[Path] = None
    folders: List["Folder"] = field(default_factory=list)
    pages: Dict[str, "Page"] = field(default_factory=dict)
    page_groups: Dict[str, "PageGroup"] = field(default_factory=dict)

    title: Optional[str] = None

    def contains_pages(self) -> bool:
        if len(self.pages) > 0:
            return True
        if len(self.page_groups) > 0:
            return True
        for f in self.folders:
            if f.contains_pages():
                return True
        return False

    def get_all_sub_pages(self) -> Sequence["Page"]:
        sub_pages: List[Page] = []
        for p in self.pages.values():
            sub_pages.append(p)
        for pg in self.page_groups.values():
            for p in pg.pages.values():
                sub_pages.append(p)
        return sub_pages

    def get_list(self, source_path: Path) -> Union[List[Any], Dict[str, Any]]:
        path = (
            self.index_path.relative_to(source_path)
            if self.index_path
            else self.path.relative_to(source_path)
        )

        sub_pages = self.get_all_sub_pages()
        if len(sub_pages) > 0 or len(self.folders) > 0:
            children = [x.get_list(source_path) for x in sub_pages]
            for folder in self.folders:
                if folder.contains_pages():
                    children.append(folder.get_list(source_path))
            return [
                {"page": str(path), "title": self.title},
                children,
            ]
        else:
            # return [{"path": str(path), "title": self.title}]
            return {"page": str(path), "title": self.title}


@dataclass
class PageGroup:
    page_group_id: str
    pages: Dict[str, "PageGroupPage"] = field(default_factory=dict)


@dataclass
class Anchor:
    ...


@dataclass
class Page:
    path: Path

    title: Optional[str] = None

    def get_items(self) -> Sequence[Anchor]:
        ...

    def get_title(self) -> str:
        if self.title is not None:
            return self.title
        return self.path.name

    def get_list(self, source_path: Path) -> Dict[str, Any]:
        # return [
        #    {"path": str(self.path.relative_to(source_path)), "title": self.get_title()}
        # ]
        return {
            "page": str(self.path.relative_to(source_path)),
            "title": self.get_title(),
        }


@dataclass
class PageGroupPage(Page):
    pages: Dict[str, "Page"] = field(default_factory=dict)

    def get_next(self) -> "PageGroupPage":
        ...

    def get_prev(self) -> "PageGroupPage":
        ...


class PageMapper:
    def __init__(self, input_path: Path, core: Core, report: Report) -> None:
        self.input_path = input_path
        self.core = core
        self.report = report
        self.root = Folder(input_path, is_root=True)
        self._scan_folder(self.root)
        self._visit_tree(self.root)

    def get_page_group_id(self, file_name: str) -> Optional[str]:
        for prefix in ["teamwork", "preparation"]:
            if file_name.startswith(prefix + "-"):
                return prefix
        return None

    def _scan_folder(self, folder: Folder):
        source_files = sorted(list(folder.path.glob("*.md")))
        # go into source files of that folder
        for source in source_files:
            page_group_id = self.get_page_group_id(source.name)
            if source.name == "index.md":
                folder.index_path = source
            elif page_group_id is None:
                page = Page(source)
                folder.pages[source.name] = page
            else:
                if page_group_id not in folder.page_groups.keys():
                    folder.page_groups[page_group_id] = PageGroup(page_group_id)
                page_group = folder.page_groups[page_group_id]
                page = PageGroupPage(source)
                page_group.pages[source.name] = page
        # go into sub folders
        for sub_folder in sorted([x for x in folder.path.iterdir() if x.is_dir()]):
            f = Folder(sub_folder)
            folder.folders.append(f)
            self._scan_folder(f)

    def _visit_tree(self, folder: Folder):
        for page in folder.pages.values():
            self._visit_page(page, self.core)
        for page_group in folder.page_groups.values():
            self._visit_page_group(page_group, self.core)
        for page_group in folder.page_groups.values():
            for page in page_group.pages.values():
                self._visit_page_group_page(page, self.core)
        for subfolder in folder.folders:
            self._visit_folder(subfolder, self.core)
        for subfolder in folder.folders:
            self._visit_tree(subfolder)

    def _visit_folder(self, folder: Folder, core: Core):
        if folder.index_path is not None:
            folder.title = self.scan_page_for_main_anchor(folder.index_path)

    def _visit_page(self, page: Page, core: Core):
        page.title = self.scan_page_for_main_anchor(page.path)

    def _visit_page_group(self, page_group: PageGroup, core: Core):
        ...

    def _visit_page_group_page(self, page: PageGroupPage, core: Core):
        page.title = self.scan_page_for_main_anchor(page.path)

    def scan_page_for_main_anchor(self, source_file_path: Path) -> str:
        for chunk in self.core.parse_file(source_file_path, True, False, None):
            if isinstance(chunk, MarkdownChunk):
                for anchor in chunk.find_anchors():
                    return anchor.strip()
        return "---"

    def get_all_folders_with_index_paths(self) -> Sequence[Folder]:
        paths: List[Folder] = []

        def local_visit_tree(folder: Folder):
            if folder.index_path is not None:
                paths.append(folder)
            for sub_folder in folder.folders:
                local_visit_tree(sub_folder)

        local_visit_tree(self.root)
        return paths
