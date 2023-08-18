from urllib.parse import quote

PLACEHOLDER_PREFIX = "_placeholder"


def svg_1(
    width: int,
    height: int,
    bgcolor: str = "eeeeee",
    textcolor: str = "aaaaaa",
) -> str:
    fontsize: int = round(
        max(12, min(min(width, height) * 0.75, (0.75 * max(width, height)) / 12))
    )
    text = f"{width}x{height}"
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"'
        + f'viewBox="0 0 {width} {height}" preserveAspectRatio="none">'
        + f'<rect width="{width}" height="{height}" fill="#{bgcolor}"/>'
        + f'<text text-anchor="middle" x="{width / 2}" y="{height / 2}" '
        + f'style="fill:#{textcolor};font-weight:bold;font-size:{fontsize}px;'
        + f'font-family:Arial,Helvetica,sans-serif;dominant-baseline:central">"{text}</text></svg>"'
    )
    # data:image/svg+xml;charset=UTF-8, svg


def svg_2(
    width: int,
    height: int,
    bgcolor: str = "eeeeee",
    textcolor: str = "aaaaaa",
) -> str:
    fontsize: int = round(
        max(12, min(min(width, height) * 0.75, (0.75 * max(width, height)) / 12))
    )
    fontfamily = "Arial,Helvetica,sans-serif"
    dy = "10.5"
    fontweight = "bold"
    text = f"{width}x{height}"
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
        + f'<rect fill="#{bgcolor}" width="{width}" height="{height}"/>'
        + f'<text fill="#{textcolor}" font-family="{fontfamily}" font-size="{fontsize}" dy="{dy}" font-weight="{fontweight}" x="50%" y="50%" text-anchor="middle">{text}</text>'
        + "</svg>"
    )


def get_placeholder_uri(width: int, height: int) -> str:
    return "data:image/svg+xml;charset=UTF-8," + quote(svg_2(width, height))


def is_placeholder(src: str) -> bool:
    return src.startswith(PLACEHOLDER_PREFIX)


def get_placeholder_uri_str(src: str) -> str:
    if is_placeholder(src):
        width, height = (100, 100)
        try:
            text = src.replace(PLACEHOLDER_PREFIX, "")
            tokens = text.split("x")
            if len(tokens) > 1:
                width, height = int(tokens[0]), int(tokens[1])
        except ValueError:
            ...
        return get_placeholder_uri(width, height)
    return src
