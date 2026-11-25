#!/usr/bin/env python3
"""Validate the skill package against the Agent Skills layout rules."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "figma-xml-to-ui"
SKILL = SKILL_DIR / "SKILL.md"

errors: list[str] = []
warnings: list[str] = []

if not SKILL.is_file():
    print("FAILED: skills/figma-xml-to-ui/SKILL.md is missing")
    sys.exit(1)

text = SKILL.read_text()
if not text.startswith("---\n"):
    print("FAILED: SKILL.md must start with YAML frontmatter")
    sys.exit(1)

_, frontmatter, body = text.split("---\n", 2)

def field(name: str) -> str | None:
    match = re.search(rf"^{name}:\s*(.+)$", frontmatter, re.MULTILINE)
    return match.group(1).strip() if match else None

name = field("name")
description = field("description")

if not name:
    errors.append("frontmatter: missing name")
elif not re.fullmatch(r"[a-z0-9-]+", name):
    errors.append(f"frontmatter: name {name!r} must be lowercase letters, digits, hyphens")
elif name != SKILL_DIR.name:
    errors.append(f"frontmatter: name {name!r} must match folder {SKILL_DIR.name!r}")

if not description:
    errors.append("frontmatter: missing description")
else:
    if len(description) > 1024:
        errors.append(f"frontmatter: description is {len(description)} chars (max 1024)")
    if not description.lower().startswith("use when"):
        warnings.append("frontmatter: description should start with 'Use when'")

if len(frontmatter) > 1024:
    errors.append(f"frontmatter: {len(frontmatter)} chars total (max 1024)")

# Every referenced relative file must exist, and every shipped reference must be referenced.
referenced = set(re.findall(r"`((?:references|assets)/[A-Za-z0-9._-]+\.(?:md|xml|png))`", body))
for rel in sorted(referenced):
    if not (SKILL_DIR / rel).exists():
        errors.append(f"SKILL.md references missing file: {rel}")

shipped = {p.relative_to(SKILL_DIR).as_posix() for p in (SKILL_DIR / "references").glob("*.md")}
unreferenced = shipped - referenced
for rel in sorted(unreferenced):
    errors.append(f"reference shipped but never mentioned in SKILL.md: {rel}")

words = len(body.split())
if words > 1100:
    warnings.append(f"SKILL.md body is {words} words; consider moving detail into references/")

for warning in warnings:
    print(f"warning: {warning}")

if errors:
    print("FAILED:")
    for err in errors:
        print(f"  - {err}")
    sys.exit(1)

print(f"skill OK: {name}, description {len(description)} chars, {words} words")
