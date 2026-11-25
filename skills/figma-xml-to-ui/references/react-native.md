# React Native Translation Rules (`TSX`)

## 1. Styling System Detection

Check `package.json` for `nativewind`.

- **NativeWind installed**: Tailwind `className` utilities with mapped theme tokens first; exact arbitrary values for anything unmapped: `p-[16px]`, `gap-[12px]`, `rounded-[14px]`, `bg-[#0F172A]`, `text-[15px] leading-[22px]`.
- **No NativeWind**: `StyleSheet.create({...})` at the bottom of the file. Unitless numbers only — never `'12px'`, never `rem`.

## 2. Primitives and Interactivity

- `<View>`, `<Text>`, `<ScrollView>`, `<SafeAreaView>`, `<Pressable>`, `<TextInput>`, `<Image>`.
- Never emit HTML tags. Never put a raw string outside `<Text>`.
- Interactive nodes (`Button`, `Btn`, `Tab`, `CardPressable`) -> `<Pressable>`, or `TouchableOpacity` when that is the repo convention. Render `disabled` from the variant when the export carries one.
- Text fields (`Input`, `TextField`, `SearchBar`) -> `<TextInput>` with the placeholder string.
- Add `accessibilityRole` from the node's semantics and `accessibilityLabel` from its visible text or layer name. Images that are decorative get `accessible={false}`.

## 3. Flexbox Layout Mapping

- `HORIZONTAL` -> `flexDirection: 'row'`; `VERTICAL` -> `'column'` (set explicitly).
- `itemSpacing` -> `gap`. **RN 0.71+ only**: if `package.json`'s RN version is lower, emit `columnGap`/`rowGap` as margins on children or a spacer View, and say which fallback you used.
- `paddingTop` / `paddingBottom` / `paddingLeft` / `paddingRight` -> same props; collapse to `paddingHorizontal` / `paddingVertical` only when both sides match.
- `horizontalPadding` / `verticalPadding` shorthand expands to both sides.
- `primaryAxisAlignItems`: `MIN` -> `justifyContent: 'flex-start'`, `CENTER` -> `'center'`, `MAX` -> `'flex-end'`, `SPACE_BETWEEN` -> `'space-between'`.
- `counterAxisAlignItems`: `MIN` -> `alignItems: 'flex-start'`, `CENTER` -> `'center'`, `MAX` -> `'flex-end'`, `BASELINE` -> `'baseline'`.
- `layoutWrap="WRAP"` -> `flexWrap: 'wrap'`.

## 4. Sizing

- `FIXED` -> explicit numeric `width` / `height` **from the node**, not recomputed.
- `HUG` -> omit the fixed dimension; add `alignSelf: 'flex-start'` when the parent would stretch it.
- `FILL` -> `flex: 1` on the parent's main axis, or `alignSelf: 'stretch'` / `width: '100%'` on the cross axis. The node's `width`/`height` is informational — do not emit it as a fixed size.
- `clipsContent="true"` -> `overflow: 'hidden'`.
- `rotation` -> `transform: [{ rotate: '8deg' }]` alongside the node's own layout position.

## 5. Fills, Strokes, Effects

Fills are child paint elements, possibly several.

- **One solid fill** -> `backgroundColor: color`. Apply the paint's `opacity` as `rgba()` or an 8-digit hex.
- **Multiple fills** -> RN has no layered background. Render the bottom-most (`fills[0]`) as the container's `backgroundColor`, then each subsequent fill as an absolutely positioned child `<View>` with matching `borderRadius`, `pointerEvents="none"`, before the content children.
- **Gradient fill** (`type` starts with `GRADIENT_`): use `expo-linear-gradient` only if it is already a dependency. Map stops in order with positions as `locations`, `start`/`end` from the gradient handles (vertical by default). If the library is absent, emit `TODO(figma): gradient on "<name>"` with the stop list and use the dominant stop as a solid — state that it is an approximation.
- **Image fill** -> `<Image source={{ uri: imageRef }} resizeMode="cover" />` when the project has a resolver; otherwise `TODO(figma): export image "<name>"` with the exact box and `scaleMode` (`FILL` -> `cover`, `FIT` -> `contain`, `CROP` -> `cover` + offset, `TILE` -> `repeat`).
- **Strokes** -> `borderColor` + numeric `borderWidth` for a single stroke. `strokeAlign="INSIDE"` matches RN's border (default). `CENTER`/`OUTSIDE` change outer size: implement with an absolutely positioned overlay View inset by `-strokeWeight / 2` (center) or `-strokeWeight` (outside), or emit a TODO with the values. Multiple strokes: first as border, rest as TODO.
- **Per-corner radii** -> `borderTopLeftRadius` etc. when the grouped `cornerRadius` is absent.
- **`DROP_SHADOW`** -> iOS `shadowColor` / `shadowOffset: { width: x, height: y }` / `shadowOpacity` (effect opacity, combined with color alpha) / `shadowRadius: radius`; Android `elevation` roughly `y + radius / 2`. Comment that elevation is an approximation.
- **`INNER_SHADOW`** -> no native support. Emit `TODO(figma): inner shadow` with values; if the repo already uses a shadow library that supports it, use that.
- **`LAYER_BLUR` / `BACKGROUND_BLUR`** -> `expo-blur` only if present, otherwise TODO. Do not fake with opacity.

## 6. Typography

- `characters` is the literal string; keep newlines, punctuation, and casing.
- Map `fontSize`, unitless `lineHeight` (**pixels/points, not a multiplier**), `letterSpacing` (convert `PERCENT` to `fontSize * value / 100`), `fontWeight` as a string, `textAlign`.
- `textAutoResize`: `WIDTH_AND_HEIGHT` -> no width; `HEIGHT` -> width fixed, height auto; `NONE` -> fixed box; `TRUNCATE` -> `numberOfLines={1}` + `ellipsizeMode="tail"`.
- RN has no vertical text alignment: when `textAlignVertical` matters, wrap the `<Text>` in a `<View>` with `justifyContent` from the value.

## 7. Icons

- PascalCase the icon name, import from `lucide-react-native`: `icon-arrow-left` -> `<ArrowLeft size={24} color="#18181B" />`.
- If `lucide-react-native` is absent, use the icon set the repo already imports.
- `size` from the node width; `color` from the icon's stroke or fill paint. For filled brand marks, use the repo's SVG asset or `TODO(figma)` with exact bounds.
