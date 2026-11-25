#!/usr/bin/env python3
"""Validate the bundled FigML fixtures and their 1:1 assumptions.

Checks:
  1. Both fixtures are well-formed and FigML-shaped (PI, <children>, no legacy content= attr).
  2. The login fixture's text is fully covered by the reference render.
  3. Auto-layout geometry adds up (padding + gaps + children == frame size), so a
     stale explicit width/height cannot silently disagree with the layout.
  4. The coverage fixture really exercises image / gradient / hidden / rotation paths.
"""

from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOGIN = ROOT / "examples" / "sample-login.xml"
CARD = ROOT / "examples" / "sample-card.xml"
PREVIEW = ROOT / "examples" / "preview.html"

TOL = 0.51
errors: list[str] = []
notes: list[str] = []


def load(path: Path) -> ET.Element:
    raw = path.read_text()
    if "<?figml" not in raw:
        errors.append(f"{path.name}: missing <?figml ...?> processing instruction")
    if "content=" in raw:
        errors.append(f"{path.name}: legacy content= attribute; FigML uses characters=")
    return ET.fromstring(raw)


def kids(node: ET.Element) -> list[ET.Element]:
    wrapper = node.find("children")
    return list(wrapper) if wrapper is not None else []


def num(node: ET.Element, name: str, default: float = 0.0) -> float:
    value = node.get(name)
    return float(value) if value is not None else default


def paint_count(node: ET.Element, container: str) -> int:
    group = node.find(container)
    return len(list(group)) if group is not None else 0


def check_geometry(node: ET.Element, path: str) -> None:
    layout = node.get("layoutMode")
    if layout not in ("HORIZONTAL", "VERTICAL"):
        for child in kids(node):
            check_geometry(child, f"{path}/{child.get('name')}")
        return

    children = kids(node)
    stroke = num(node, "strokeWeight") * 2
    horizontal = layout == "HORIZONTAL"
    size = num(node, "width") if horizontal else num(node, "height")
    pad_a = num(node, "paddingLeft" if horizontal else "paddingTop")
    pad_b = num(node, "paddingRight" if horizontal else "paddingBottom")
    if node.get("horizontalPadding") and horizontal:
        pad_a = pad_b = num(node, "horizontalPadding")
    if node.get("verticalPadding") and not horizontal:
        pad_a = pad_b = num(node, "verticalPadding")

    gap = num(node, "itemSpacing") * max(0, len(children) - 1)
    inner = size - stroke - pad_a - pad_b
    fills = [c for c in children if c.get(
        "layoutSizingHorizontal" if horizontal else "layoutSizingVertical") == "FILL"]
    fixed = sum(
        num(c, "width" if horizontal else "height")
        for c in children
        if c not in fills
    )

    if not children or size == 0:
        pass
    elif len(fills) == 1:
        expected = inner - gap - fixed
        actual = num(fills[0], "width" if horizontal else "height")
        if actual == 0:
            # Flex spacer: design-time size is 0, main axis absorbs the remainder.
            notes.append(f"{path}: spacer {fills[0].get('name')!r} absorbs {expected:g} on the main axis")
        elif abs(expected - actual) > TOL:
            errors.append(
                f"{path}: FILL child {fills[0].get('name')!r} is {actual:g} but layout gives "
                f"{expected:g} (size {size:g}, stroke {stroke:g}, padding {pad_a:g}/{pad_b:g}, gap {gap:g})"
            )
    elif not fills:
        total = fixed + gap + pad_a + pad_b + stroke
        if total > size + TOL:
            errors.append(f"{path}: children need {total:g} but frame is {size:g}")

    for child in children:
        check_geometry(child, f"{path}/{child.get('name')}")


def main() -> int:
    login = load(LOGIN)
    card = load(CARD)
    if login.tag != "frame":
        errors.append(f"sample-login.xml: root <{login.tag}> is not <frame>")

    # 3. Geometry
    check_geometry(login, "Login")
    check_geometry(card, "Card")

    # 2. Text coverage against the reference render
    preview = PREVIEW.read_text()
    for text in login.iter("Text"):
        chars = text.get("characters") or ""
        for line in chars.split("\n"):
            if line and line not in preview:
                errors.append(f"preview.html is missing text {line!r} from {text.get('name')!r}")

    # 4. Coverage fixture really covers the hard paths
    visible_false = [n for n in card.iter() if n.get("visible") == "false"]
    if not visible_false:
        errors.append("sample-card.xml: expected at least one visible=\"false\" node")
    gradient = [n for n in card.iter("fill") if (n.get("type") or "").startswith("GRADIENT_")]
    if not gradient:
        errors.append("sample-card.xml: expected a GRADIENT_* fill")
    image = [n for n in card.iter("fill") if n.get("type") == "IMAGE"]
    if not image:
        errors.append("sample-card.xml: expected an IMAGE fill")
    rotated = [n for n in card.iter() if n.get("rotation")]
    if not rotated:
        errors.append("sample-card.xml: expected a rotated node")

    if notes:
        print("\n".join(notes))
    if errors:
        print("FAILED:")
        for err in errors:
            print(f"  - {err}")
        return 1
    print("examples OK: schema, geometry, preview coverage, and coverage paths")
    return 0


if __name__ == "__main__":
    sys.exit(main())
