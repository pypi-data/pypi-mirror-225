import random
import re
from pathlib import Path
from typing import List, Optional

from .report import Report

ENV_PATTERN = re.compile("[a-zA-Z]*:")


def has_class_tag(s_line: str) -> bool:
    return s_line.startswith(":") and ENV_PATTERN.match(s_line) is not None


def none_str(string_or_none: Optional[str]) -> str:
    return string_or_none if string_or_none else ""


def write_file(content: str, target_file_path: Path, report: Report):
    encoding = "utf-8"
    try:
        with open(target_file_path, "w", encoding=encoding) as file:
            file.write(content)
    except UnicodeEncodeError as error:
        report.tell(
            f"Encoding error when writing file {target_file_path}.",
            level=Report.ERROR,
        )
        character = error.object[error.start : error.end]
        line = content.count("\n", 0, error.start) + 1
        report.tell(
            "Character {} in line {} cannot be saved with encoding {}.".format(
                character, line, encoding
            ),
            level=Report.ERROR,
        )
        with open(target_file_path, "w", encoding=encoding, errors="ignore") as file:
            file.write(content)


# for recoding chunks
def remove_empty_lines_begin_and_end(code: str) -> str:
    lines = code.splitlines()
    start = 0
    for i, line in enumerate(lines):
        if line.strip():
            start = i
            break
    end = len(lines)
    for i, line in enumerate(lines[::-1]):
        if line.strip():
            end = len(lines) - i
            break
    return "\n".join(lines[start:end])


def random_id():
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=5))


def add_notnone(content: Optional[str], collector: List[str]):
    if content is not None:
        collector.append(content)


def reverse_path(parent_path: Path, child_path: Path) -> str:
    levels = len(child_path.relative_to(parent_path).parent.parts)
    s = ""
    for _ in range(levels):
        s = "../" + s
    return s


def get_common_base(path1: Path, path2: Path) -> Path:
    common = []
    for p1, p2 in zip(path1.parts, path2.parts):
        if p1 == "/":
            ...
        elif p1 == p2:
            common.append(p1)
        else:
            break
    return Path("/" + "/".join(common))


def get_relative_path(path1: Path, path2: Path) -> Path:
    base_path = get_common_base(path1, path2)
    return reverse_path(base_path, path1) / path2.relative_to(base_path)
