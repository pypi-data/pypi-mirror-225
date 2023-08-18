from pathlib import Path
from typing import Any, Dict, List

import requests

from ... import Builder, RawChunk, YAMLChunk, YamlExtension, HTMLChunk


def download_preview(url: str, target_path: Path):
    if not target_path.exists():
        data = requests.get(url).content
        with open(target_path, "wb") as handler:
            handler.write(data)


class VideoExtension(YamlExtension):
    def __init__(self):
        super().__init__(type=["video", "youtube"], chunk_class=Video)


class Video(YAMLChunk):
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
            required=["video"],
            optional=["start", "caption", "position"],
        )
        if "caption" in self.dictionary:
            ...
            self.asides.insert(
                0,
                HTMLChunk.create_derived_chunk(
                    self.dictionary["caption"],
                    # builder.convert(
                    #     self.dictionary["caption"],
                    #     target_format="html",
                    #     source_format="md",
                    # ),
                    self.raw_chunk,
                ),
            )

    def get_id(self):
        video = self.dictionary["video"]
        return super().create_hash(f"{video}")

    def to_html(self, builder: Builder, target_file_path: Path):
        html: List[str] = []
        video = self.dictionary["video"]
        url = f"https://youtube-nocookie.com/{video}"
        # url = "https://youtu.be/{}".format(video)
        start = ""
        if "start" in self.dictionary:
            start = "?start={}".format(self.dictionary["start"])
            url = url + start
        if "position" in self.dictionary and self.dictionary["position"] == "aside":
            aside_id = self.get_id()
            html.append(f'<span name="{aside_id}"></span><aside name="{aside_id}">')
            html.append(
                '<a href="{}"><img width="{}" src="https://img.youtube.com/vi/{}/sddefault.jpg"></img></a>'.format(
                    url, 240, video
                )
            )
            # if "caption" in self.dictionary:
            #     html.append(
            #         builder.convert(
            #             self.dictionary["caption"],
            #             target_format="html",
            #             source_format="md",
            #         )
            #     )
            html.append("</aside>")
        else:
            html.append('<div class="figure">')
            width = 560
            height = 315
            # TODO set the title element of an iframe to improve accessibility scores
            html.append(
                '<iframe width="{}" height="{}" src="https://www.youtube-nocookie.com/embed/{}{}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'.format(
                    width, height, video, start
                )
            )
            # if "caption" in self.dictionary:
            #     html.append(
            #         '<span name="{}">&nbsp;</span>'.format(self.dictionary["video"])
            #     )
            #     html.append(
            #         '<aside name="{}"><p>{}</p></aside>'.format(
            #             self.dictionary["video"],
            #             builder.convert(
            #                 self.dictionary["caption"],
            #                 target_format="html",
            #                 source_format="md",
            #             ),
            #         )
            #     )
            html.append("</div>")
        return "\n".join(html)

    def to_latex(self, builder: Builder) -> str:
        s: List[str] = []
        url = "https://img.youtube.com/vi/{}/sddefault.jpg".format(
            self.dictionary["video"]
        )
        video_url = "https://youtu.be/{}".format(self.dictionary["video"])
        video_id = self.get_id()
        target_path = self.get_dir_cached() / f"{video_id}.jpg"
        download_preview(url, target_path)
        # target_path =  Path('../cached/{}.jpg'.format(video_id))
        target_path = target_path.relative_to(builder.output_file.parent)
        s.append(r"\n")
        s.append(r"\\begin{video}[h]")
        s.append(rf"\includegraphics[width=\linewidth]{{{target_path}}}")
        if "caption" in self.dictionary:
            s.append(
                r"\caption{"
                + builder.convert(
                    self.dictionary["caption"],
                    target_format="latex",
                    source_format="md",
                )
                + r" \textcolor{SteelBlue}{\faArrowCircleRight}~"
                + rf"\\url{{{video_url}}}"
                + r"}"
            )
        else:
            s.append(r"\caption{")
            s.append(rf"\\url{{{video_url}}}" + "}")
        s.append(r"\end{video}")
        return r"\n".join(s)
