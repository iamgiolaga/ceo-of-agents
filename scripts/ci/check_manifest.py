#!/usr/bin/env python3
"""Validate the plugin manifest and the marketplace file.

- .claude-plugin/plugin.json: kebab-case name, X.Y.Z version, description.
- .claude-plugin/marketplace.json: name, owner name, and a plugins list whose
  entry for this plugin points to a folder holding this plugin.json, with the
  same name (and the same version, if the entry sets one).
- skills/<name>/SKILL.md: frontmatter with name equal to the folder name and a
  description.
- Every tracked line marked x-release-please-version (the files that
  release-please bumps, see release-please-config.json) carries the version in
  plugin.json.
Needs PyYAML.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")


def nonempty_str(value):
    return isinstance(value, str) and value.strip() != ""


def main():
    errors = []
    plugin_path = ROOT / ".claude-plugin" / "plugin.json"
    market_path = ROOT / ".claude-plugin" / "marketplace.json"
    plugin = json.loads(plugin_path.read_text(encoding="utf-8"))
    market = json.loads(market_path.read_text(encoding="utf-8"))

    name = plugin.get("name")
    if not (nonempty_str(name) and KEBAB.match(name)):
        errors.append(f"plugin.json: name {name!r} is not kebab-case")
    if not (nonempty_str(plugin.get("version")) and SEMVER.match(plugin["version"])):
        errors.append(f"plugin.json: version {plugin.get('version')!r} is not X.Y.Z")
    if not nonempty_str(plugin.get("description")):
        errors.append("plugin.json: description is missing")
    if "author" in plugin and not nonempty_str((plugin["author"] or {}).get("name")):
        errors.append("plugin.json: author.name is missing")
    if "keywords" in plugin and not all(nonempty_str(k) for k in plugin["keywords"]):
        errors.append("plugin.json: keywords must be non-empty strings")

    if not (nonempty_str(market.get("name")) and KEBAB.match(market["name"])):
        errors.append(f"marketplace.json: name {market.get('name')!r} is not kebab-case")
    if not nonempty_str((market.get("owner") or {}).get("name")):
        errors.append("marketplace.json: owner.name is missing")
    entries = market.get("plugins")
    if not isinstance(entries, list) or not entries:
        errors.append("marketplace.json: plugins must be a non-empty list")
        entries = []
    names = [e.get("name") for e in entries if isinstance(e, dict)]
    if len(names) != len(set(names)):
        errors.append("marketplace.json: plugin names are not unique")
    for entry in entries:
        if not isinstance(entry, dict) or not nonempty_str(entry.get("name")):
            errors.append("marketplace.json: every plugin needs a name")
            continue
        source = entry.get("source")
        if isinstance(source, str):
            target = (ROOT / source).resolve()
            manifest = target / ".claude-plugin" / "plugin.json"
            if not manifest.is_file():
                errors.append(f"marketplace.json: {entry['name']}: source {source!r} has no .claude-plugin/plugin.json")
            elif manifest.resolve() == plugin_path.resolve():
                if entry["name"] != name:
                    errors.append(f"marketplace.json: entry {entry['name']!r} points to plugin {name!r}")
                if "version" in entry and entry["version"] != plugin.get("version"):
                    errors.append(f"marketplace.json: version {entry['version']} differs from plugin.json {plugin.get('version')}")
        elif not isinstance(source, dict):
            errors.append(f"marketplace.json: {entry['name']}: source is missing")
    if name not in names:
        errors.append(f"marketplace.json: no entry for plugin {name!r}")

    skills = sorted((ROOT / "skills").glob("*/SKILL.md"))
    for skill in skills:
        text = skill.read_text(encoding="utf-8")
        end = text.find("\n---", 3)
        meta = yaml.safe_load(text[4:end]) if text.startswith("---\n") and end != -1 else None
        where = skill.relative_to(ROOT)
        if not isinstance(meta, dict):
            errors.append(f"{where}: no frontmatter")
            continue
        if meta.get("name") != skill.parent.name:
            errors.append(f"{where}: name {meta.get('name')!r} differs from folder {skill.parent.name!r}")
        if not nonempty_str(meta.get("description")):
            errors.append(f"{where}: description is missing")

    marked = subprocess.run(
        ["git", "grep", "-n", "-I", "x-release-please-version", "--", ":!scripts/ci/*", ":!release-please-config.json", ":!CONTRIBUTING.md"],
        cwd=ROOT, capture_output=True, text=True,
    ).stdout.splitlines()
    for hit in marked:
        where, lineno, line = hit.split(":", 2)
        found = re.search(r"\d+\.\d+\.\d+", line)
        if not found or found.group(0) != plugin.get("version"):
            errors.append(f"{where}:{lineno}: version {found.group(0) if found else 'missing'} differs from plugin.json {plugin.get('version')}")
    if not marked:
        errors.append("no line is marked x-release-please-version")

    for error in errors:
        print(f"error: {error}")
    print(f"plugin {name} {plugin.get('version')}; {len(entries)} marketplace entries; {len(skills)} skills; {len(marked)} marked version lines; {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
