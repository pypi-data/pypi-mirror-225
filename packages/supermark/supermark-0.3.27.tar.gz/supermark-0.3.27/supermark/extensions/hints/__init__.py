from pathlib import Path
from typing import Any, Dict, List

from ... import Builder, ParagraphExtension, RawChunk, YAMLChunk, YamlExtension


# class HintParagraphExtension(ParagraphExtension):
#    def __init__(self):
#        super().__init__("hints", extra_tags=["hint"])


class HintExtension(YamlExtension):
    def __init__(self):
        super().__init__(type=["hints", "hint"], chunk_class=Hint)


class Hint(YAMLChunk):
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
            optional=["title", "image"],
        )
        self.title = dictionary["title"] if "title" in dictionary else ""
        if "image" in dictionary:
            self.image_file = (
                self.raw_chunk.path.parent / Path(dictionary["image"])
            ).resolve()
            if not self.image_file.exists():
                self.tell("Image does not exist.", self.WARNING)
                self.image_file = None
        else:
            self.image_file = None
        if self.has_post_yaml():
            self.hint = self.get_post_yaml()
        elif self.image_file is None:
            self.tell(
                "Hint should have a post-yaml section with the content.", self.WARNING
            )
            self.hint = ""

    def to_html(self, builder: Builder, target_file_path: Path):
        html: List[str] = []
        html.append(f'<button class="w3collapsible">{self.title}</button>')
        html.append('<div class="w3content">')

        if self.image_file is not None:
            builder.copy_resource(self.raw_chunk, self.image_file)
            html.append(f'<img src="{self.dictionary["image"]}" width="100%"/>')
        else:
            html.append(
                builder.convert(self.hint, target_format="html", source_format="md")
            )
        html.append("</div>")
        return "\n".join(html)

    def to_latex(self, builder: Builder):
        latex: List[str] = []
        # TODO
        return "\n".join(latex)
