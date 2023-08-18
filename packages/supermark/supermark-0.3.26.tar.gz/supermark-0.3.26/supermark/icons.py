import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Optional

icons: Dict[str, str] = {}


def load_bootstrap_icons():
    path = Path(__file__).parent / "data/bootstrap-icons.svg"

    ET.register_namespace("", "http://www.w3.org/2000/svg")
    # ET.register_namespace("", "http://www.w3.org/2000/svg")
    tree = ET.parse(path)
    root = tree.getroot()
    # print(root)
    for child in root:
        xml = (
            ET.tostring(
                child,
                encoding="utf-8",
            )
            .decode("utf-8")
            .replace("<symbol ", "<svg ")
            .replace("</symbol>", "</svg>")
            .replace("\n", "")
        )
        # print(xml.replace('"', "'"))
        icons[child.get("id")] = xml
        # break
        # print(child.get("id"))

    # print(load_bootstrap_icons.__doc__)

    # replace currentcolor with color

    # print(child.get("id"))
    # print("----")
    # print(ET.tostring(child))
    # ET.dump(child)
    # print("----")
    # print(icons["x-diamond-fill"])
    # for childchild in child:  # <symbol id="">
    #    print(childchild.tag)
    #    print(childchild.get("id"))
    # print(), child.attrib)

    # print(icons.keys())


def get_icon(icon: str, size: Optional[str] = None) -> str:
    if len(icons) == 0:
        load_bootstrap_icons()
    if icon in icons:
        svg = icons[icon]
        if size is not None:
            return svg.replace("xmlns=", f'width="{size}" height="{size}" xmlns=')
        return svg

    return ""


load_bootstrap_icons()
