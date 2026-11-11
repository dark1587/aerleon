"""Lint tests for the hand-written usage pages under docs/.

Step 3 appends "docs/api/**/*.md" to OWNED_PAGE_GLOBS.
"""

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
OWNED_PAGE_GLOBS = ["docs/getting_started.md", "docs/usage/**/*.md"]
GENERATORS_PAGE = REPO_ROOT / "docs/reference/generators.md"
MERMAID_CLASSES_REF = '--8<-- "docs/snippets/mermaid-classes.mmd"'

SNIPPET_RE = re.compile(r'^\s*-+8<-+\s+"([^"]+)"')
FENCE_RE = re.compile(r"^(\s*)(`{3,}|~{3,})(.*)$")
OUTPUT_ADMONITION_RE = re.compile(r'^(\s*)\?\?\?\+?\s+example\s+"Output"')
INTERNAL_LINK_RE = re.compile(r"(?<!_)\[[^\]]+\]\((?!https?:)[^)]*\.md[^)]*\)(?!_)")


def owned_pages() -> list[Path]:
    pages: set[Path] = set()
    for pattern in OWNED_PAGE_GLOBS:
        pages.update(p for p in REPO_ROOT.glob(pattern) if p.is_file())
    return sorted(pages)


def _page_id(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def snippet_refs(text: str) -> list[tuple[str, str | None]]:
    refs = []
    for line in text.splitlines():
        match = SNIPPET_RE.match(line)
        if not match:
            continue
        target = match.group(1)
        if ":" in target:
            path, _, section = target.rpartition(":")
            refs.append((path, section))
        else:
            refs.append((target, None))
    return refs


def _fences(text: str):
    """Yield (info, body_lines, opening_line_index) for every fenced block."""
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        match = FENCE_RE.match(lines[i])
        if not match:
            i += 1
            continue
        marker = match.group(2)
        info = match.group(3).strip()
        start = i
        body = []
        i += 1
        while i < len(lines):
            close = FENCE_RE.match(lines[i])
            if close and close.group(2)[0] == marker[0] and not close.group(3).strip():
                break
            body.append(lines[i])
            i += 1
        i += 1
        yield info, body, start


def strip_fences(text: str) -> str:
    """Return text with every fenced code block (fences included) removed."""
    lines = text.splitlines()
    drop: set[int] = set()
    for _info, body, start in _fences(text):
        drop.update(range(start, start + len(body) + 2))
    return "\n".join(line for n, line in enumerate(lines) if n not in drop)


def mermaid_blocks(text: str) -> list[list[str]]:
    return [body for info, body, _ in _fences(text) if info == "mermaid"]


def output_block_bodies(text: str) -> list[list[str]]:
    lines = text.splitlines()
    blocks = []
    for info, body, start in _fences(text):
        fence_indent = len(FENCE_RE.match(lines[start]).group(1))
        # Walk back to the nearest preceding line with smaller indentation that
        # is not blank; that is the block's parent.
        parent = None
        for j in range(start - 1, -1, -1):
            line = lines[j]
            if not line.strip():
                continue
            indent = len(line) - len(line.lstrip())
            if indent < fence_indent:
                parent = line
                break
        if parent is not None and OUTPUT_ADMONITION_RE.match(parent):
            blocks.append([line for line in body if line.strip()])
    return blocks


# ---------------------------------------------------------------- parser self-tests


def test_snippet_refs_with_section():
    assert snippet_refs('    --8<-- "docs/a.md:sec"\n') == [("docs/a.md", "sec")]


def test_snippet_refs_without_section():
    assert snippet_refs('--8<-- "docs/a.yaml"') == [("docs/a.yaml", None)]


def test_mermaid_blocks_in_tab():
    text = (
        '=== "Tab"\n'
        "\n"
        "    ```mermaid\n"
        "    graph LR\n"
        "      a --> b\n"
        "    ```\n"
    )
    assert mermaid_blocks(text) == [["    graph LR", "      a --> b"]]


def test_output_block_bodies_only_under_output_admonition():
    text = (
        '=== "Cisco"\n'
        "\n"
        "    ```yaml\n"
        "    not: output\n"
        "    ```\n"
        "\n"
        '    ??? example "Output"\n'
        "\n"
        "        ```\n"
        '        --8<-- "docs/examples/cli/x/expected/a.acl"\n'
        "        ```\n"
    )
    assert output_block_bodies(text) == [
        ['        --8<-- "docs/examples/cli/x/expected/a.acl"']
    ]


def test_strip_fences_removes_code():
    text = "a\n```\n[x](y.md)\n```\nb"
    assert strip_fences(text) == "a\nb"


# ---------------------------------------------------------------- page tests

PAGES = owned_pages()
PAGE_PARAMS = [pytest.param(p, id=_page_id(p)) for p in PAGES]


@pytest.mark.parametrize("path", PAGE_PARAMS)
def test_snippet_references_resolve(path):
    for ref, section in snippet_refs(path.read_text()):
        target = REPO_ROOT / ref
        assert target.exists(), f"{ref} does not exist"
        if section:
            content = target.read_text()
            assert f"[start:{section}]" in content, f"{ref} lacks [start:{section}]"
            assert f"[end:{section}]" in content, f"{ref} lacks [end:{section}]"


@pytest.mark.parametrize("path", PAGE_PARAMS)
def test_mermaid_blocks_use_shared_classes(path):
    for body in mermaid_blocks(path.read_text()):
        non_blank = [line for line in body if line.strip()]
        assert non_blank, "empty mermaid block"
        assert non_blank[-1].strip() == MERMAID_CLASSES_REF
        assert not any("classDef" in line for line in body)
        assert not any("<span" in line for line in body)


@pytest.mark.parametrize("path", PAGE_PARAMS)
def test_output_blocks_are_embedded(path):
    for body in output_block_bodies(path.read_text()):
        for line in body:
            refs = snippet_refs(line)
            assert refs, f"output block line is not an embed: {line!r}"
            ref = refs[0][0]
            assert "/expected/" in ref or ref.endswith(".stdout.ref"), ref


@pytest.mark.parametrize("path", PAGE_PARAMS)
def test_no_inheritance_word(path):
    assert "inheritance" not in strip_fences(path.read_text()).lower()


@pytest.mark.parametrize("path", PAGE_PARAMS)
def test_internal_links_are_italic(path):
    matches = INTERNAL_LINK_RE.findall(strip_fences(path.read_text()))
    assert not matches, f"non-italic internal links: {matches}"


# ---------------------------------------------------------------- drift test


def _between_markers(text: str, name: str = "sample-terms") -> list[str] | None:
    lines = text.splitlines()
    start = end = None
    for n, line in enumerate(lines):
        if f"[start:{name}]" in line:
            start = n
        elif f"[end:{name}]" in line:
            end = n
    if start is None or end is None or end < start:
        return None
    return lines[start + 1 : end]


def _example_yaml_with_markers() -> list[Path]:
    root = REPO_ROOT / "docs/examples"
    if not root.is_dir():
        return []
    return sorted(
        p for p in root.rglob("*.yaml") if "[start:sample-terms]" in p.read_text()
    )


_GENERATORS_TERMS = _between_markers(GENERATORS_PAGE.read_text())
@pytest.mark.parametrize(
    "path",
    [
        pytest.param(p, id=_page_id(p))
        for p in _example_yaml_with_markers()
    ],
)
def test_running_example_terms_match_generators_sample(path):
    assert _GENERATORS_TERMS is not None, "generators.md lacks sample-terms markers"
    assert _between_markers(path.read_text()) == _GENERATORS_TERMS
