#!/usr/bin/env python3
"""Check relative links in tracked Markdown files.

A relative link must point to a file that exists. An anchor to a Markdown file
(`#section`, `other.md#section`) must match one of its headings, using the
same slugs as GitHub. External links (http, https, mailto) are skipped on
purpose: checking them depends on the network and makes CI flaky. Links inside
code blocks, inline code and template placeholders ({{...}}) are ignored.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

INLINE_LINK = re.compile(r"!?\[(?:[^\[\]]|\[[^\]]*\])*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
REF_DEF = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*<?(\S+?)>?(?:\s+.*)?$")
HTML_ATTR = re.compile(r"<(?:a|img|source|video)\b[^>]*?\s(?:href|src)=\"([^\"]+)\"", re.IGNORECASE)
FENCE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE = re.compile(r"`+[^`]*`+")
SKIP_PREFIXES = ("http://", "https://", "mailto:", "data:")
HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(.*?)\s*#*\s*$")
HTML_ID = re.compile(r"<[^>]+\s(?:id|name)=\"([^\"]+)\"")


def tracked_markdown():
    out = subprocess.run(
        ["git", "ls-files", "-z", "--", "*.md"],
        cwd=ROOT, check=True, capture_output=True, text=True,
    ).stdout
    return [ROOT / p for p in out.split("\0") if p]


def slugify(heading):
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", heading)  # keep link text
    text = re.sub(r"<[^>]+>", "", text).replace("`", "")
    text = re.sub(r"[^\w\- ]", "", text.strip().lower())
    return text.replace(" ", "-")


_anchor_cache = {}


def anchors(path):
    if path not in _anchor_cache:
        found, counts, in_fence = set(), {}, False
        for line in path.read_text(encoding="utf-8").splitlines():
            if FENCE.match(line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            found.update(HTML_ID.findall(line))
            match = HEADING.match(line)
            if match:
                slug = slugify(match.group(1))
                n = counts.get(slug, 0)
                counts[slug] = n + 1
                found.add(slug if n == 0 else f"{slug}-{n}")
        _anchor_cache[path] = found
    return _anchor_cache[path]


def targets(text):
    in_fence = False
    for lineno, line in enumerate(text.splitlines(), start=1):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        line = INLINE_CODE.sub("", line)
        for regex in (INLINE_LINK, HTML_ATTR):
            for match in regex.finditer(line):
                yield lineno, match.group(1)
        ref = REF_DEF.match(line)
        if ref:
            yield lineno, ref.group(1)


def main():
    errors = []
    checked = 0
    for path in tracked_markdown():
        text = path.read_text(encoding="utf-8")
        for lineno, target in targets(text):
            if target.startswith(SKIP_PREFIXES) or "{{" in target or "$" in target:
                continue
            clean, _, anchor = target.partition("#")
            clean = clean.split("?", 1)[0]
            if clean:
                base = ROOT if clean.startswith("/") else path.parent
                resolved = (base / clean.lstrip("/")).resolve()
            else:
                resolved = path
            checked += 1
            where = f"{path.relative_to(ROOT)}:{lineno}"
            if not resolved.exists():
                errors.append(f"{where}: broken relative link: {target}")
            elif anchor and resolved.suffix == ".md" and anchor not in anchors(resolved):
                errors.append(f"{where}: no heading for anchor: {target}")
    for error in errors:
        print(error)
    print(f"{checked} relative links checked, {len(errors)} broken")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
