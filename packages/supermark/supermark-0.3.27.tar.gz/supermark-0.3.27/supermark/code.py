from pathlib import Path
from typing import Any, Dict, List, Sequence

from pygments import highlight
from pygments.formatters import LatexFormatter
from pygments.lexers import get_lexer_by_name

from .chunks import Builder, Chunk, RawChunk


class Code(Chunk):
    def __init__(self, raw_chunk: RawChunk, page_variables: Dict[str, Any]):
        super().__init__(raw_chunk, page_variables)
        if self.get_first_line().startswith("```"):
            self.lang = self.get_first_line().replace("```", "").strip()
            self.code = "".join(self.raw_chunk.lines[1:-1])
        else:
            self.lang = None
            self.code = self.get_content()

    def get_chunk_type(self) -> str:
        return "code" if self.lang is None else f"code/{self.lang}"

    def wrap_in_code_frame(self, code: str, builder: Builder) -> str:
        html: List[str] = []
        raw_id = "id" + Chunk.create_hash(self.code)
        html.append('<div class="source-code-frame mt-3 mb-3">')
        html.append(f'<pre class="d-none" id="{raw_id}">{self.code}</pre>')
        html.append(
            f'<button type="button" class="copy-button" data-clipboard-target="#{raw_id}">'
        )
        html.append(
            '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-clipboard" viewBox="0 0 16 16">'
        )
        html.append(
            '  		<path d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1v-1z"></path>'
        )
        html.append(
            '  		<path d="M9.5 1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5h3zm-3-1A1.5 1.5 0 0 0 5 1.5v1A1.5 1.5 0 0 0 6.5 4h3A1.5 1.5 0 0 0 11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3z"></path>'
        )
        html.append("	</svg>")
        html.append("</button>")
        html.append(code)
        html.append("</div>")
        return "\n".join(html)

    def to_html(self, builder: Builder, target_file_path: Path) -> str:
        # lexer = None
        # if self.lang is not None:
        #     try:
        #         lexer = get_lexer_by_name(self.lang, stripall=True)
        #     except Exception as e:
        #         print(e)
        # output: List[str] = []
        # if lexer is not None:
        #     formatter = HtmlFormatter()
        #     output.append(highlight(self.code, lexer, formatter))
        #     return "\n".join(output)
        return self.wrap_in_code_frame(
            builder.convert_code(self.get_content(), target_format="html"), builder
        )

    def to_latex(self, builder: Builder) -> str:
        lexer = None
        if self.lang is not None:
            try:
                lexer = get_lexer_by_name(self.lang, stripall=True)
            except Exception as e:
                print(e)
        output: List[str] = []
        if lexer is not None:
            formatter = LatexFormatter(linenos=False, verboptions="breaklines")
            output.append(highlight(self.code, lexer, formatter))
        else:
            output.append(r"\begin{Verbatim}[breaklines]")
            output.append(self.code)
            output.append(r"\end{Verbatim}")
        return "\n".join(output)

    def recode(self) -> str:
        # import was failing on Github actions, therefore here
        import black

        if self.get_first_line().startswith("```"):
            lang = self.get_first_line().replace("```", "").strip()
            code = "".join(self.raw_chunk.lines[1:-1])
            if lang == "python":
                try:
                    code = black.format_str(code, mode=black.Mode())
                except black.InvalidInput as e:
                    print(e)
            return "```" + lang + "\n" + code + "```"
        else:
            return self.get_content()
