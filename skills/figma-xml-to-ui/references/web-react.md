# React.js / Vite.js / Next.js Translation Rules (`TSX`)

## 1. Framework and Styling Detection

- **Next.js** (`next` in `package.json`): with the App Router (`app/`), add `'use client';` at the top only when the file uses event handlers or React hooks. Use `next/image` / `next/link` when the project already does; otherwise plain `<img>` and `<a>`.
- **Tailwind** (`tailwindcss` in `package.json`): mapped theme utilities first; exact arbitrary values for anything unmapped — `p-[16px]`, `gap-[12px]`, `rounded-[12px]`, `bg-[#18181B]`, `text-[15px] leading-[22px]`.
- **No Tailwind**: CSS Modules (`ComponentName.module.css`) or style objects with explicit `px` units.

## 2. Semantic Primitives

- Use semantic HTML: `<main>`, `<section>`, `<header>`, `<nav>`, `<div>`, `<span>`, `<p>`, `<button>`, `<input>`.
- Interactive nodes (`Button`, `Btn`, `Tab`) -> `<button type="button">`. Text fields (`Input`, `SearchBar`) -> `<input>`.
- Text nodes keep their own tag (`<p>` or `<span>`) — do not flatten everything into `<div>`.

## 3. Flexbox Layout Mapping

- `layoutMode="HORIZONTAL"` -> `flex flex-row`
- `layoutMode="VERTICAL"` -> `flex flex-col`
- `itemSpacing` -> `gap-[{n}px]`
- `primaryAxisAlignItems`: `MIN` -> `justify-start`, `CENTER` -> `justify-center`, `MAX` -> `justify-end`, `SPACE_BETWEEN` -> `justify-between`
- `counterAxisAlignItems`: `MIN` -> `items-start`, `CENTER` -> `items-center`, `MAX` -> `items-end`

## 4. Sizing (`layoutSizingHorizontal` / `layoutSizingVertical`)

- `FIXED` -> `w-[{n}px] h-[{n}px]`
- `HUG` -> `w-fit h-fit`
- `FILL` -> `flex-1` on the parent's main axis, or `w-full` / `self-stretch` on the cross axis

## 5. Typography, Borders, Shadows

- Map `fontSize`, `lineHeight`, `letterSpacing`, `fontWeight`, `textAlignHorizontal`, `color` directly in `px` / hex.
- `clipsContent="true"` -> `overflow-hidden`.
- `DROP_SHADOW` -> exact CSS `box-shadow: {x}px {y}px {blur}px {spread}px {rgba}`.
- Per-corner radii -> `rounded-tl-[..]` style utilities or `border-radius` shorthand with four values.

## 6. Icons

- PascalCase the icon name and import from `lucide-react`: `icon-search` -> `<Search className="w-[16px] h-[16px] text-[#71717A]" />`.
- Size comes from the XML node width/height; color from the stroke or fill.
