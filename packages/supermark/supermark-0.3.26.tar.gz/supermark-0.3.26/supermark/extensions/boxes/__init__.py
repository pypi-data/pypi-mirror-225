from typing import Optional, Sequence
from ... import ParagraphExtension, MarkdownChunk, Builder, div


class BoxParagraphExtension(ParagraphExtension):
    def __init__(self, tag: str = "", extra_tags: Optional[Sequence[str]] = None):
        super().__init__(tag, extra_tags=extra_tags)

    def build_html(self, chunk: MarkdownChunk, builder: Builder) -> str:
        return div(
            builder.convert(
                chunk.get_content(), target_format="html", source_format="md"
            ),
            classes=[self.tag, "box", "mt-3", "mb-3"],
        )


class FactBoxParagraphExtension(BoxParagraphExtension):
    def __init__(self):
        super().__init__("factbox", extra_tags=["note-box"])


class MilestoneParagraphExtension(BoxParagraphExtension):
    def __init__(self):
        super().__init__("milestone")


class DefinitionParagraphExtension(BoxParagraphExtension):
    def __init__(self):
        super().__init__("definition")


class DeliveryParagraphExtension(BoxParagraphExtension):
    def __init__(self):
        super().__init__("delivery")


class GuidelineParagraphExtension(BoxParagraphExtension):
    def __init__(self):
        super().__init__("guideline")


class ReportParagraphExtension(BoxParagraphExtension):
    def __init__(self):
        super().__init__("report")


class WarningParagraphExtension(BoxParagraphExtension):
    def __init__(self):
        super().__init__("warning")


class TipParagraphExtension(BoxParagraphExtension):
    def __init__(self):
        super().__init__("tip")


class TaskParagraphExtension(BoxParagraphExtension):
    def __init__(self):
        super().__init__("task")
