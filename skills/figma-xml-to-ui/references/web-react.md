# React.js / Vite.js / Next.js Translation Rules (`TSX`)

## 1. Framework and Styling Detection

- **Next.js** (`next` in `package.json`): with the App Router (`app/`), add `'use client';` only when the file uses event handlers or hooks. Use `next/image` / `next/link` when the project already does; otherwise plain `<img>` and `<a>`.
- **Tailwind**: mapped theme utilities first; exact arbitrary values for anything unmapped — `p-[16px]`, `gap-[12px]`, `rounded-[12px]`, `bg-[#18181B]`, `text-[15px] leading-[22px]`.
- **No Tailwind**: CSS Modules (`ComponentName.module.css`) or style objects with explicit `px`.

## 2. Semantic Primitives and Accessibility

- `<main>`, `<section>`, `<header>`, `<nav>`, `<div>`, `<span>`, `<p>`, `<h1>`–`<h6>`.
- Interactive nodes -> `<button type="button">`; text fields -> `<input>` with the placeholder.
- Images need `alt` (from the layer name or surrounding text) or `alt=""` when decorative.
- Keep native focus behavior; do not remove outlines. If the design has no focus style, add the repo's existing one.

## 3. Flexbox Layout Mapping

- `HORIZONTAL` -> `flex flex-row`; `VERTICAL` -> `flex flex-col`.
- `itemSpacing` -> `gap-[{n}px]`; `layoutWrap="WRAP"` -> `flex-wrap`.
- `primaryAxisAlignItems`: `MIN` -> `justify-start`, `CENTER` -> `justify-center`, `MAX` -> `justify-end`, `SPACE_BETWEEN` -> `justify-between`.
- `counterAxisAlignItems`: `MIN` -> `items-start`, `CENTER` -> `items-center`, `MAX` -> `items-end`, `BASELINE` -> `items-baseline`.
- Negative gaps are not valid CSS — use margins instead and note it.

## 4. Sizing

- `FIXED` -> `w-[{n}px] h-[{n}px]`.
- `HUG` -> `w-fit h-fit`.
- `FILL` -> `flex-1` on the main axis, or `w-full` / `self-stretch` on the cross axis. Ignore the design-time width/height for FILL nodes.
- `clipsContent="true"` -> `overflow-hidden`.
- `rotation` -> `rotate-[{deg}deg]` or `transform: rotate({deg}deg)`.

## 5. Fills, Strokes, Effects

- **Fills are bottom-up, CSS backgrounds are top-down.** `fills[0]` is the bottom-most paint and must be the **last** layer in `background`/`background-image`. Getting this backwards hides every solid under a gradient.
- Multiple solid fills -> `background: linear-gradient(colorTop, colorTop), colorBottom;` or stacked `background-image` layers, with `background-repeat: no-repeat`.
- **Gradient fill** -> `linear-gradient({angle}deg, stop1 p1%, stop2 p2%)`. Figma `GRADIENT_LINEAR` uses handle positions; angle = `atan2(dx, -dy)` in degrees, normalized, then mapped to CSS (0deg = to top, 90deg = to right). Convert stop `opacity` to `rgba()` or 8-digit hex. `GRADIENT_RADIAL` -> `radial-gradient(circle at {x}% {y}%, ...)`. Angular/diamond have no exact CSS twin — approximate with `conic-gradient` and call it out.
- **Image fill** -> `<img src={asset} className="absolute inset-0 h-full w-full object-cover" />` or `background-image: url(...); background-size: cover`. `scaleMode`: `FILL` -> `cover`, `FIT` -> `contain`, `TILE` -> `repeat`. No asset -> `TODO(figma)` with the exact box.
- **Strokes**: `border: {w}px solid {color}` for `INSIDE` (with `box-sizing: border-box`, which Tailwind preflight provides). `OUTSIDE` -> `outline: {w}px solid {color}; outline-offset: 0` (outline never affects layout). `CENTER` -> border plus `outline-offset: -{w/2}px` or a pseudo-element; state the technique used.
- Per-corner radii -> `rounded-tl-[..]` etc. or `border-radius: tl tr br bl`.
- **`DROP_SHADOW`** -> `box-shadow: {x}px {y}px {blur}px {spread}px {rgba}`; multiple effects comma-joined.
- **`INNER_SHADOW`** -> same syntax with `inset`.
- **`LAYER_BLUR`** -> `filter: blur({radius/2}px)`; **`BACKGROUND_BLUR`** -> `backdrop-filter: blur(...)` (check browser targets before relying on it).
- **`blendMode` on the node** -> `mix-blend-mode`; on a paint, it is not a CSS blend mode — treat as opacity only.
- **Opacity inheritance**: CSS `opacity` already composites the subtree. Set it on the parent only; never multiply it into children as well.

## 6. Typography

- `characters` is literal, including newlines (`white-space: pre-line` when the source has line breaks).
- `fontSize`, `lineHeight`, `letterSpacing` in `px`; `letterSpacing` `PERCENT` -> `{fontSize * value / 100}px`; `fontWeight` numeric maps directly.
- `textAlignHorizontal` -> `text-align`; `textAlignVertical` -> flex alignment on the wrapper.
- `textAutoResize`: `NONE` -> fixed `width`/`height`; `HEIGHT` -> `width` fixed, height auto; `TRUNCATE` -> `white-space: nowrap; overflow: hidden; text-overflow: ellipsis`.
- Map heading-sized text to real heading tags when the node's name says so (`Heading`, `Title`, `H1`); otherwise `<p>`/`<span>`.

## 7. Icons

- PascalCase the name, import from `lucide-react`: `icon-search` -> `<Search className="w-[16px] h-[16px] text-[#71717A]" />`.
- Size from the node width/height, color from the stroke or fill paint.
- Brand marks (Google, Apple, logos) are not in icon libraries — use the repo's SVG asset or `TODO(figma)` with exact bounds.
