# FigML Format Reference

Read this before translating any FigML export. It defines what the XML actually looks like, so the pipeline maps real nodes instead of guessed attribute names.

Source of truth: the official example at <https://ai-integration-dev.github.io/figml-docs/examples> plus the plugin's settings docs. Where this file labels something **(inferred)**, the official docs do not show it — trust the user's export over this file and say so.

## Identifying a FigML export

- XML declaration, then `<?figml version="1.0"?>` processing instruction.
- Root is a single `<frame>` (or the selected node's tag).
- Children are wrapped: `<children> ... </children>`. Paint, effect, and layout metadata are child elements, **not** attributes.
- Node tag is the **Figma component name** for instances: a component named `Button` exports as `<Button>`, `h-icon_solid_heart` as `<h-icon_solid_heart>`. Do not assume tag names from a fixed list — read `type="..."`.
- `type` is authoritative: `FRAME`, `INSTANCE`, `TEXT`, `VECTOR`, `RECTANGLE`, `GROUP`, `ELLIPSE`, `BOOLEAN_OPERATION`, `COMPONENT`, `COMPONENT_SET`.

If the root, the `<?figml?>` instruction, or the `<children>` wrapper is missing, stop and confirm the exporter and version before generating code.

## Geometry

- `x`, `y` are absolute coordinates **relative to the parent**, in points/pixels. Use them only for nodes without `layoutMode`; inside auto-layout, order and spacing win.
- `width`, `height` are the design-time size. When `layoutSizingHorizontal`/`layoutSizingVertical` is `FILL`, the value is informational — the parent's flex rules decide the final size. Trust `FILL` over the number.
- `layoutSizingHorizontal` / `layoutSizingVertical`: `FIXED`, `HUG`, `FILL`.
- `rotation` (degrees) and `opacity` are omitted when default because "omit default values" is on by default.

## Auto-layout attributes

| Attribute | Meaning |
|---|---|
| `layoutMode` | `HORIZONTAL` / `VERTICAL`; absent = absolute-positioned children |
| `itemSpacing` | gap between children |
| `paddingTop` / `paddingBottom` / `paddingLeft` / `paddingRight` | also `horizontalPadding` / `verticalPadding` shorthand when symmetric |
| `primaryAxisAlignItems` | `MIN`, `CENTER`, `MAX`, `SPACE_BETWEEN` |
| `counterAxisAlignItems` | `MIN`, `CENTER`, `MAX`, `BASELINE` |
| `layoutWrap` | `WRAP` means flex-wrap |
| `clipsContent` | `true` -> clip overflow |
| `cornerRadius` | grouped form; when "group related properties" is off, read `topLeftRadius`, `topRightRadius`, `bottomLeftRadius`, `bottomRightRadius` |

"Group related properties" also collapses `strokeTopWeight` / `strokeRightWeight` / ... into `strokeWeight`. Both forms are valid input — handle whichever appears.

## Paint containers

Fills and strokes are child elements. One container can hold **multiple paints**, applied bottom-up:

```xml
<fills>
  <fill blendMode="NORMAL" color="#ffbe00" />
</fills>
<strokes>
  <stroke blendMode="NORMAL" color="#E4E4E7" />
</strokes>
```

Figma paint types you must recognize (inferred shapes; verify against the export):

- Solid: `color="#RRGGBB"` (+ optional `opacity`).
- Gradient: `type="GRADIENT_LINEAR|GRADIENT_RADIAL|GRADIENT_ANGULAR|GRADIENT_DIAMOND"`, stop list under `<gradientStops>`, geometry under `<gradientHandlePositions>` or `<gradientTransform>`.
- Image: `type="IMAGE"` with `imageRef` and `scaleMode` (`FILL`, `FIT`, `CROP`, `TILE`).

`blendMode` on a paint is not the layer blend mode; layer blending lives on the node (`blendMode`, default `PASS_THROUGH`, omitted).

Stroke placement comes from `strokeAlign` on the node: `INSIDE` (Figma default), `OUTSIDE`, `CENTER`. This changes rendered size per platform — never ignore it.

## Effects

```xml
<effects>
  <effect type="DROP_SHADOW" radius="2" spread="0" blendMode="NORMAL"
          showShadowBehindNode="false" color="#000000">
    <offset x="0" y="1" />
  </effect>
</effects>
```

Types: `DROP_SHADOW`, `INNER_SHADOW`, `LAYER_BLUR`, `BACKGROUND_BLUR`. Color alpha is sometimes a separate attribute — check for `opacity` or an 8-digit hex before assuming full opacity.

## Text

Text content is `characters`, not an element body:

```xml
<Text id="I1189:5212;7:7637" name="Button" type="TEXT"
      characters="Button" fontSize="12" fontWeight="600"
      textAlignHorizontal="CENTER" textAutoResize="WIDTH_AND_HEIGHT"
      width="39" height="12">
  <fills><fill blendMode="NORMAL" color="#000000" /></fills>
  <fontName family="Inter" style="Semi Bold" />
  <letterSpacing value="0" unit="PERCENT" />
  <lineHeight value="12" unit="PIXELS" />
</Text>
```

- `fontWeight` is numeric (100–900). `fontName` carries family + style; prefer `family`/`style` when the project already registers that font, otherwise fall back to the numeric weight.
- `letterSpacing.unit` may be `PERCENT` or `PIXELS`; convert percent to `fontSize * value / 100`.
- `lineHeight.unit` may be `PIXELS`, `PERCENT`, or `AUTO`. `AUTO` means font default — omit it, do not guess.
- `textAutoResize`: `WIDTH_AND_HEIGHT` = hug, `HEIGHT` = fixed width + auto height, `NONE` = fixed box (needs explicit wrapping), `TRUNCATE` = single line with ellipsis.
- `textAlignVertical` may appear (`TOP`, `CENTER`, `BOTTOM`).
- Newlines inside `characters` are literal `\n` — preserve them.

## Components and instances

- An instance carries `type="INSTANCE"`, its component name as the tag, and a `<mainComponent id="..."/>` reference.
- `<variantProperties ...>` holds the variant selection; `<componentProperties>` holds nested prop values (TEXT overrides, booleans, instance swaps). Use these as props when the repo has a matching component.
- If the export embeds a `<COMPONENT>` or `<COMPONENT_SET>` definition (master), it is a library definition, **not** screen UI. Skip it unless the user asks for the component itself.
- `visible="false"` nodes are hidden in Figma. Omit them from output; never render them "for completeness".

## Unknown or lossy constructs

The exporter may drop things you need (vector path data when "simplify vector paths" is on, images that were not exported, gradient handles under a different element name). When a construct is present but its shape is unrecognized:

1. Do not guess a mapping.
2. Emit a `TODO(figma): <node name> — unsupported <thing>` comment at that position, including the raw XML snippet.
3. Keep the node's box (width/height) so layout still matches.
4. Report every TODO in the final message.

Never silently drop a node. Never invent a value to make the output look complete.
