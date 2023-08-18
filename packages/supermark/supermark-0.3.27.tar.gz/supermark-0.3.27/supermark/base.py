from abc import abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Sequence, List

from .write_html import HTMLTable

if TYPE_CHECKING:
    from .chunks import Chunk


class ExtensionPoint:
    """Base class for any extension point."""

    def __init__(self, name: str):
        self.name = name


class Extension:
    def __init__(self):
        self.folder = None
        self.package = None
        self.extension_point = None

    def set_folder(self, folder: Path):
        self.folder = folder

    def set_extension_point(self, extension_point: ExtensionPoint):
        self.extension_point = extension_point

    def set_package(self, package: "ExtensionPackage"):
        self.package = package

    @abstractmethod
    def get_name(self):
        ...

    def _find_files(self, pattern: str):
        return list(self.folder.glob(pattern))

    def files_to_string(self, files: Sequence[Path]) -> str:
        string: str = ""
        for file in files:
            with open(file, encoding="utf-8", errors="surrogateescape") as open_file:
                string += open_file.read()
        return string

    def get_css(self) -> str:
        return self.files_to_string(self._find_files("*.css"))

    def get_js(self) -> str:
        return self.files_to_string(self._find_files("*.js"))

    def get_examples(self):
        return self._find_files("example-*.md")

    def get_doc(self) -> Optional[Path]:
        files = self._find_files("doc.md")
        if len(files) > 0:
            return files[0]
        return None

    def get_doc_summary(self) -> Optional[str]:
        doc = self.get_doc()
        if doc is None:
            return None
        docstring = doc.read_text()
        if len(docstring.strip()) == 0:
            return None
        sentences = docstring.strip().split(".")
        return sentences[0].strip()

    def __str__(self) -> str:
        return "Extension at " + str(self.folder)

    def get_spec_html(self) -> str:
        return ""

    @abstractmethod
    def get_doc_table(
        self, example_chunks: Optional[Sequence["Chunk"]] = None
    ) -> HTMLTable:
        ...


class ExtensionPackage:
    def __init__(self, folder: Path):
        self.folder = folder
        self.extensions: List[Extension] = []
        alpha_file = folder / "alpha.md"
        self.alpha = alpha_file.exists()

    def is_alpha(self) -> bool:
        return self.alpha

    def register_extension(self, extension: Extension):
        self.extensions.append(extension)

    def _find_files(self, pattern: str):
        return list(self.folder.glob(pattern))

    def files_to_string(self, files: Sequence[Path]) -> str:
        string: str = ""
        for file in files:
            with open(file, encoding="utf-8", errors="surrogateescape") as open_file:
                string += open_file.read()
        return string

    def get_css(self) -> str:
        return self.files_to_string(self._find_files("*.css"))

    def get_js(self) -> str:
        return self.files_to_string(self._find_files("*.js"))

    def get_examples(self):
        return self._find_files("example-*.md")

    def get_doc(self) -> Optional[Path]:
        files = self._find_files("doc.md")
        if len(files) > 0:
            return files[0]
        return None

    def get_doc_summary(self) -> Optional[str]:
        doc = self.get_doc()
        if doc is None:
            return None
        docstring = doc.read_text()
        if len(docstring.strip()) == 0:
            return None
        sentences = docstring.strip().split(".")
        return sentences[0].strip()

    def __str__(self) -> str:
        return "Extension at " + str(self.folder)
