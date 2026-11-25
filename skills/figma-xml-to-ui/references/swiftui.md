# SwiftUI Translation Rules (`Swift`)

## 1. Layout Containers and Alignment

- `HORIZONTAL` -> `HStack(alignment: ..., spacing: {itemSpacing})`
  - `counterAxisAlignItems`: `MIN` -> `.top`, `CENTER` -> `.center`, `MAX` -> `.bottom`, `BASELINE` -> `.firstTextBaseline`
- `VERTICAL` -> `VStack(alignment: ..., spacing: {itemSpacing})`
  - `counterAxisAlignItems`: `MIN` -> `.leading`, `CENTER` -> `.center`, `MAX` -> `.trailing`
- **No `layoutMode`** -> `ZStack(alignment: .topLeading)` with `.offset(x: ..., y: ...)` per child, using `x`/`y` relative to the parent's border box. Subtract the parent's padding only when the export's coordinates include it.
- **Distribution**: `SPACE_BETWEEN` -> `Spacer()` between children; `MAX` -> leading `Spacer()`; `CENTER` -> `Spacer()` on both ends.
- **`layoutWrap="WRAP"`** -> `LazyVGrid` or a wrapping `Layout`; a plain `HStack` does not wrap.
- **Scrolling**: wrap a root taller than the screen in `ScrollView(.vertical, showsIndicators: false)`.

## 2. Modifier Order (critical for 1:1 parity)

1. Content and typography: `.font(...)`, `.foregroundStyle(...)`, `.tracking(...)`, `.lineSpacing(...)`
2. Inner padding: `.padding(EdgeInsets(top: ..., leading: ..., bottom: ..., trailing: ...))`
3. Frame and sizing: `FIXED` -> `.frame(width:height:)`; `FILL` -> `.frame(maxWidth: .infinity)` / `.frame(maxHeight: .infinity)`; `HUG` -> omit `.frame()` or `.fixedSize()`
4. Background and clipping: `.background(...)`, `.clipShape(RoundedRectangle(cornerRadius: ...))`
5. Border: `.overlay(...)` — **`.strokeBorder`, not `.stroke`** (see below)
6. Shadow: `.shadow(color:radius:x:y:)`
7. Transform: `.rotationEffect(.degrees({rotation}))`, then `.opacity(...)` when the node itself is translucent

Padding after a frame, or a background before the frame, changes the rendered size and breaks parity.

## 3. Fills, Strokes, Effects

- **Solid fill(s)**: one fill -> `.background(color)` or `.background(color, in: RoundedRectangle(cornerRadius: r))`. Several fills -> `ZStack` with the bottom-most fill first (`fills[0]` is bottom-most), each clipped to the same shape.
- **Gradient** -> `LinearGradient(gradient: Gradient(stops: [...]), startPoint: .top, endPoint: .bottom)`. Derive the direction from the gradient handles; default vertical. `GRADIENT_RADIAL` -> `RadialGradient`; angular/diamond -> `AngularGradient` with a note when it differs.
- **Image fill** -> `Image("{asset}").resizable().scaledToFill().clipped()` (`FILL`), `.scaledToFit()` (`FIT`). No asset -> `TODO(figma)` with the exact box.
- **Strokes** — `strokeAlign` decides the API:
  - `INSIDE` (default): `.overlay(RoundedRectangle(cornerRadius: r).strokeBorder(color, lineWidth: w))` — `strokeBorder` draws **inside** the shape.
  - `CENTER`: `.overlay(RoundedRectangle(cornerRadius: r).stroke(color, lineWidth: w))` — half the width hangs outside, matching Figma.
  - `OUTSIDE`: expand the overlay shape by `w / 2` and use `strokeBorder`, e.g. `RoundedRectangle(cornerRadius: r + w/2).strokeBorder(...).padding(-w/2)`; verify visually because it grows the hit area.
  - Never use `.stroke` for an `INSIDE` stroke: it adds `w / 2` outside the bounds.
- **`DROP_SHADOW`** / **`INNER_SHADOW`**: `.shadow(color: color.opacity(alpha), radius: radius / 2, x: x, y: y)` for outer shadows (`radius / 2` because Figma's blur is roughly two sigma). Inner shadows have no modifier: use an inverse-masked overlay or emit `TODO(figma)` with the values.
- **`LAYER_BLUR`** -> `.blur(radius: radius / 2)`; **`BACKGROUND_BLUR`** -> `.background(.ultraThinMaterial)` only when the repo already uses materials, otherwise TODO.
- **Opacity inheritance**: `.opacity()` applies to the whole subtree, which matches Figma. Set it on the parent only.

## 4. Typography and Colors

- `.font(.system(size: {fontSize}, weight: .{weight}))` where 100–300 -> `.light`, 400 -> `.regular`, 500 -> `.medium`, 600 -> `.semibold`, 700 -> `.bold`, 800–900 -> `.heavy`/`.black`.
- Custom family from `<fontName family="..." style="..."/>` only when the project registers it; otherwise fall back to the system font and say so.
- `.lineSpacing(max(0, lineHeight - fontSize))` — SwiftUI adds spacing rather than setting total line height.
- `.tracking(letterSpacing)`; convert `PERCENT` to `fontSize * value / 100`.
- `textAutoResize`: `HEIGHT`/`WIDTH_AND_HEIGHT` -> let it grow; `NONE` -> `.frame(width:height:)` + `.lineLimit(nil)`; `TRUNCATE` -> `.lineLimit(1).truncationMode(.tail)`.
- Prefer `Color("TokenName")` or `Color.theme.*` on exact matches; otherwise an exact hex initializer. Add the `private extension Color { init(hex:) }` helper only when the project has none.

## 5. Interactivity, Icons, Accessibility

- Interactive nodes -> `Button(action: { ... }) { ... }.buttonStyle(.plain)`.
- Inputs -> `TextField("{placeholder}", text: $binding)`.
- **SF Symbols**: `icon-arrow-left` -> `arrow.left`, `icon-search` -> `magnifyingglass`, `icon-mail` -> `envelope`, `icon-lock` -> `lock`, `icon-eye` -> `eye`. Size with `.font(.system(size: {width}))`, color with `.foregroundStyle(...)`.
- No matching symbol or brand mark -> keep `Image("{asset}")` with `TODO(figma): add asset`, never a lookalike.
- Add `.accessibilityLabel(...)` for icon-only buttons and `.accessibilityHidden(true)` for decorative art.
