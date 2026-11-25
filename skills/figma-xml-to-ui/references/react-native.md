# React Native Translation Rules (`TSX`)

## 1. Styling System Detection

Check `package.json` for `nativewind`.

- **NativeWind installed**: use Tailwind `className` utilities with mapped theme tokens first. Use exact arbitrary values for anything unmapped: `p-[16px]`, `gap-[12px]`, `rounded-[14px]`, `bg-[#0F172A]`, `text-[15px] leading-[22px]`.
- **No NativeWind**: `StyleSheet.create({...})` at the bottom of the file. Unitless numbers only — never `'12px'`, never `rem`.

## 2. Primitives and Interactivity

- Use `<View>`, `<Text>`, `<ScrollView>`, `<SafeAreaView>`, `<Pressable>`, `<TextInput>`, `<Image>`.
- Never emit HTML tags (`<div>`, `<span>`, `<p>`, `<button>`).
- Never put a raw string outside `<Text>`.
- Wrap interactive nodes (`Button`, `Btn`, `Tab`, `CardPressable`) in `<Pressable>` — or `TouchableOpacity` when that is the repo's convention.
- Text fields (`Input`, `SearchBar`, `TextField`) become `<TextInput>`, with `placeholder` from the XML placeholder string.

## 3. Flexbox Layout Mapping

- `layoutMode="HORIZONTAL"` -> `flexDirection: 'row'`
- `layoutMode="VERTICAL"` -> `flexDirection: 'column'` (set it explicitly)
- `itemSpacing` -> unitless `gap`
- `paddingTop` / `paddingBottom` / `paddingLeft` / `paddingRight` -> same numeric props; collapse to `paddingHorizontal` / `paddingVertical` only when both sides match
- `primaryAxisAlignItems`: `MIN` -> `justifyContent: 'flex-start'`, `CENTER` -> `'center'`, `MAX` -> `'flex-end'`, `SPACE_BETWEEN` -> `'space-between'`
- `counterAxisAlignItems`: `MIN` -> `alignItems: 'flex-start'`, `CENTER` -> `'center'`, `MAX` -> `'flex-end'`

## 4. Sizing (`layoutSizingHorizontal` / `layoutSizingVertical`)

- `FIXED` -> explicit numeric `width` / `height`
- `HUG` -> omit the fixed dimension; add `alignSelf: 'flex-start'` when the parent would otherwise stretch it
- `FILL` -> `flex: 1` on the parent's main axis, or `alignSelf: 'stretch'` / `width: '100%'` on the cross axis

## 5. Typography, Borders, Shadows

- **Typography**: map `fontSize`, numeric unitless `lineHeight`, `letterSpacing`, `fontWeight` as a string (`'400'`..`'700'`), `textAlignHorizontal` -> `textAlign` (`'left'` / `'center'` / `'right'`), and `color`.
- **Clipping and borders**: `clipsContent="true"` -> `overflow: 'hidden'`. Strokes -> `borderColor` plus numeric `borderWidth`. Radii -> numeric `borderRadius`, or per-corner `borderTopLeftRadius` etc. when they differ.
- **Shadows**: a `DROP_SHADOW` effect needs both platforms:
  - iOS: `shadowColor`, `shadowOffset: { width: x, height: y }`, `shadowOpacity`, `shadowRadius`
  - Android: `elevation` (derive as roughly `y + blur / 2`, and mention the approximation in a comment)
  - NativeWind: use `shadow-*` utilities only if the project already configures them; otherwise fall back to the style object.

## 6. Icons

- PascalCase the icon name and import from `lucide-react-native`: `icon-arrow-right` -> `<ArrowRight size={20} color="#F8FAFC" />`.
- If `lucide-react-native` is not installed, use `@expo/vector-icons` (check which set the repo imports).
- Pass `size` from the XML node's width, and `color` from the node's stroke/fill.
