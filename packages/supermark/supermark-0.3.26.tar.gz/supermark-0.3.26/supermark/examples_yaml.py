from typing import Any, List, Sequence, Set

from .chunks import Chunk, YAMLChunk, YAMLDataChunk, YAMLGroupChunk
from .write_html import HTMLTable, html_link


class YAMLExamples:
    """Handles a set of examples of YAML chunks, to query them for specs."""

    def __init__(self, chunks: Sequence[Chunk]) -> None:
        self.chunks = chunks

    def has_yaml_groups(self) -> bool:
        return len(self.get_yaml_groups()) > 0

    def get_yaml_groups(self) -> Sequence[YAMLGroupChunk]:
        groups: List[YAMLGroupChunk] = []
        for chunk in self.chunks:
            if isinstance(chunk, YAMLGroupChunk):
                groups.append(chunk)
        return groups

    def get_yaml_chunks(self) -> Sequence[YAMLChunk]:
        """No yaml groups or data chunks"""
        groups: List[YAMLChunk] = []
        for chunk in self.chunks:
            if isinstance(chunk, YAMLGroupChunk):
                for c in chunk.chunks:
                    groups.append(c)
            elif isinstance(chunk, YAMLDataChunk):
                ...
            elif isinstance(chunk, YAMLChunk):
                groups.append(chunk)
        return groups

    def get_all_chunks(self) -> Sequence[YAMLChunk]:
        chunks: List[YAMLChunk] = []
        chunks.extend(self.get_yaml_groups())
        chunks.extend(self.get_yaml_chunks())
        return chunks

    def get_chunk_classes(self) -> set[Any]:
        types: Set[Any] = set()
        for chunk in self.get_yaml_chunks():
            types.add(type(chunk))
        return types

    def get_group_classes(self) -> set[Any]:
        types: Set[Any] = set()
        for chunk in self.get_yaml_groups():
            types.add(type(chunk))
        return types

    def get_types(self, type: Any) -> Set[str]:
        types: Set[str] = set()
        for chunk in filter(lambda c: isinstance(c, type), self.get_all_chunks()):
            types.add(str(chunk.dictionary["type"]))
        return types

    def get_required(self, type: Any) -> Sequence[str]:
        for chunk in filter(lambda c: isinstance(c, type), self.get_all_chunks()):
            return chunk.required
        return []

    def get_optional(self, type: Any) -> Sequence[str]:
        for chunk in filter(lambda c: isinstance(c, type), self.get_all_chunks()):
            return chunk.optional
        return []

    def has_post_yaml(self, type: Any) -> str:
        found_with_post_yaml: bool = False
        found_without_post_yaml: bool = False
        for chunk in filter(lambda c: isinstance(c, type), self.get_all_chunks()):
            if chunk.has_post_yaml():
                found_with_post_yaml = True
            else:
                found_without_post_yaml = True
        if found_with_post_yaml and not found_without_post_yaml:
            return "required"
        elif found_with_post_yaml and found_without_post_yaml:
            return "optional"
        else:
            return "no"

    def get_doc_table_yaml(self, type: Any) -> HTMLTable:
        table: HTMLTable = HTMLTable(css_class="table")
        table.add_row("Python type", type.__name__)
        table.flush_row()
        table.add_row("type", ", ".join(list(self.get_types(type))))
        table.flush_row()
        table.add_row("Language", html_link("#", "YAML"))
        table.flush_row()
        table.add_row("Required fields", ", ".join(self.get_required(type)))
        table.flush_row()
        table.add_row("Optional fields", ", ".join(self.get_optional(type)))
        table.flush_row()
        table.add_row("Post-Yaml Section", self.has_post_yaml(type))
        table.flush_row()
        return table

    def write_doc(self, md: List[str]):
        md.append("\n\n\n")
        for group_class in self.get_group_classes():
            table = self.get_doc_table_yaml(group_class)
            table.flush_row_group()
            md.append(table.get_html())
            md.append("\n\n\n")
        for chunk_class in self.get_chunk_classes():
            table = self.get_doc_table_yaml(chunk_class)
            table.flush_row_group()
            md.append(table.get_html())
            md.append("\n\n\n")
