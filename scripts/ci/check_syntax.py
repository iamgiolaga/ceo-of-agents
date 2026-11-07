#!/usr/bin/env python3
"""Check that every tracked JSON and YAML file parses, and that the YAML
frontmatter of every tracked Markdown file parses.

Template placeholders such as {{ORG_ID}} are replaced with a plain word before
parsing, so templates are checked as the YAML they become once rendered.
Needs PyYAML.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
PLACEHOLDER = re.compile(r"\{\{[A-Za-z0-9_]+\}\}")


def tracked(*patterns):
    out = subprocess.run(
        ["git", "ls-files", "-z", "--", *patterns],
        cwd=ROOT, check=True, capture_output=True, text=True,
    ).stdout
    return [ROOT / p for p in out.split("\0") if p]


def no_duplicate_keys(pairs):
    seen = {}
    for k, v in pairs:
        if k in seen:
            raise ValueError(f"duplicate key {k!r}")
        seen[k] = v
    return seen


def frontmatter(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        raise ValueError("frontmatter has no closing ---")
    return text[4:end]


def main():
    errors = []
    counts = {"json": 0, "yaml": 0, "frontmatter": 0}
    for path in tracked("*.json"):
        counts["json"] += 1
        try:
            json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicate_keys)
        except ValueError as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
    for path in tracked("*.yml", "*.yaml"):
        counts["yaml"] += 1
        try:
            yaml.safe_load(PLACEHOLDER.sub("placeholder", path.read_text(encoding="utf-8")))
        except yaml.YAMLError as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid YAML: {exc}")
    for path in tracked("*.md"):
        try:
            block = frontmatter(path.read_text(encoding="utf-8"))
            if block is None:
                continue
            counts["frontmatter"] += 1
            data = yaml.safe_load(PLACEHOLDER.sub("placeholder", block))
            if not isinstance(data, dict):
                raise ValueError("frontmatter is not a mapping")
        except (yaml.YAMLError, ValueError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid frontmatter: {exc}")
    for error in errors:
        print(error)
    print(f"{counts['json']} JSON, {counts['yaml']} YAML, {counts['frontmatter']} frontmatter blocks checked, {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
