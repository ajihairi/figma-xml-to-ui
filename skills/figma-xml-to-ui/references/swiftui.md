# SwiftUI Translation Rules (`Swift`)

## 1. Layout Containers and Alignment

- `layoutMode="HORIZONTAL"` -> `HStack(alignment: ..., spacing: {itemSpacing})`
  - `counterAxisAlignItems`: `MIN` -> `.top`, `CENTER` -> `.center`, `MAX` -> `.bottom`
- `layoutMode="VERTICAL"` -> `VStack(alignment: ..., spacing: {itemSpacing})`
  - `counterAxisAlignItems`: `MIN` -> `.leading`, `CENTER` -> `.center`, `MAX` -> `.trailing`
- **Frames without auto-layout** (overlapping children) -> `ZStack(alignment: .topLeading)` with `.offset(x: ..., y: ...)` per child, computed from each child's absolute position relative to the parent.
- **Distribution**: `primaryAxisAlignItems="SPACE_BETWEEN"` -> insert `Spacer()` between children. `"MAX"` -> leading `Spacer()`. `"CENTER"` -> `Spacer()` on both ends.
- **Scrolling**: wrap a root container whose height exceeds the screen in `ScrollView(.vertical, showsIndicators: false)`.

## 2. Modifier Order (critical for 1:1 parity)

Always apply modifiers in this order:

1. Content and typography: `.font(...)`, `.foregroundStyle(...)`, `.tracking(...)`, `.lineSpacing(...)`
2. Inner padding: `.padding(EdgeInsets(top: ..., leading: ..., bottom: ..., trailing: ...))`
3. Frame and sizing: `FIXED` -> `.frame(width: ..., height: ...)`; `FILL` -> `.frame(maxWidth: .infinity)` / `.frame(maxHeight: .infinity)`; `HUG` -> omit `.frame()` or use `.fixedSize()`
4. Background and clipping: `.background(...)`, `.clipShape(RoundedRectangle(cornerRadius: ...))`
5. Border overlay: `.overlay(RoundedRectangle(cornerRadius: ...).stroke(..., lineWidth: ...))`
6. Drop shadow: `.shadow(color: ..., radius: ..., x: ..., y: ...)`

Applying padding after the frame, or a background before the frame, changes the rendered size and breaks parity.

## 3. Typography and Colors

- `.font(.system(size: {fontSize}, weight: .{weight}))`, or the project's registered custom font family when the XML names one.
- `.lineSpacing(max(0, lineHeight - fontSize))` — SwiftUI adds spacing rather than setting total line height.
- `.tracking(letterSpacing)` for letter spacing.
- Prefer `Color("TokenName")` or `Color.theme.*` when a 1:1 token exists; otherwise use an exact hex initializer. Define `private extension Color { init(hex: String) }` only when the project has no existing helper.

## 4. Interactivity and Icons

- Interactive nodes (`Button`, `Btn`, `Tab`) -> `Button(action: { ... }) { ... }.buttonStyle(.plain)`.
- Input nodes (`Input`, `TextField`) -> `TextField("{placeholder}", text: $binding)`.
- **SF Symbols**: map vector icon names to the closest symbol — `icon-arrow-left` -> `arrow.left`, `icon-search` -> `magnifyingglass`, `icon-mail` -> `envelope`, `icon-eye` -> `eye` — then size with `.font(.system(size: {width}))` and color with `.foregroundStyle(...)`.
- Where no SF Symbol exists, keep `Image("{asset-name}")` with a `TODO: add asset` comment instead of substituting a wrong symbol.
