from typing import List


def nav_link_back(title: str, href: str, md: List[str]):
    md.append("\n\n\n")
    md.append("---")
    md.append("type: nav")
    md.append(f'prev: ["{title}", "{href}"]')
    md.append("---\n\n\n")
