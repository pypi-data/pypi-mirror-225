import re
from typing import TYPE_CHECKING, Optional

import pypandoc
from markdown_it import MarkdownIt
from packaging import version
from rich import print

from .icons import get_icon
from .report import Report

if TYPE_CHECKING:
    from .core import Core


md = MarkdownIt()

pattern = re.compile("{{:.*?:}}")


def print_pandoc_info(report: Report):
    installed_pandoc_version = pypandoc.get_pandoc_version()
    if installed_pandoc_version != "2.12":
        report.warning(
            f"The recommended Pandoc version is 2.12. You have version {installed_pandoc_version}. This may lead to slightly different output, when different versions commit to a repository."
        )
    else:
        report.info(f"Installed Pandoc version: {installed_pandoc_version}")
    # if version.parse(installed_pandoc_version) < version.parse("2.14"):
    #    print(
    #        "There exists a newer version of Pandoc. Update via [link=https://pandoc.org]pandoc.org[/link]."
    #    )
    # print(pypandoc.get_pandoc_path())
    # print(pypandoc.get_pandoc_formats())


def convert(
    source: str,
    target_format: str,
    core: "Core",
    source_format: str = "md",
) -> str:
    if source_format == "md" and target_format == "html":
        result = str(md.render(source))
        if "{{:" in result:
            result = _replace_variables(result, core)
        return result

    if source_format == "mediawiki":
        extra_args = ["--from", "mediawiki", "--to", "html"]
    else:
        extra_args = []
    return pypandoc.convert_text(
        source, target_format, format=source_format, extra_args=extra_args
    ).strip()


def _find_replacement(variable: str, core: "Core") -> Optional[str]:
    if variable.startswith("bi-"):
        replacement = get_icon(variable.replace("bi-", ""), size="16px")
        return replacement
    else:
        return core.config.get_replacement(variable)


def _replace_variables(input: str, core: "Core") -> str:
    if "{{:" not in input:
        return input
    string: str = input
    # find all the template variables
    variables: set[str] = set()
    for variable in re.findall(pattern, input):
        variables.add(variable[3:-3])
    # replace the found template variables
    for variable in variables:
        wrapped = "{{:" + variable + ":}}"
        replacement = _find_replacement(variable, core)
        if replacement is None or replacement == "":
            replacement = wrapped
            # TODO report missing replacement
            print(f"Replacement not found for variable {variable} {wrapped}")
        string = string.replace(wrapped, replacement)
    return string


def convert_code(source: str, target_format: str) -> str:
    extra_args = ["--highlight-style", "pygments"]

    return (
        pypandoc.convert_text(
            source, target_format, format="md", extra_args=extra_args
        ).strip()
        # This reduced difference between Pandoc results from version 2.12 and newer versions.
        .replace('<pre\nclass="sourceCode', '<pre class="sourceCode')
    )
