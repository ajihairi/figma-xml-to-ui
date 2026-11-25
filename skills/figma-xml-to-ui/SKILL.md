---
name: figma-xml-to-ui
description: Use when converting an exported Figma XML file (FigML or similar) into 1:1 UI code for React Native, React.js, Vite.js, Next.js, or SwiftUI, or when a screenshot/Figma frame must be reproduced pixel-accurately from XML with design-token, icon, and existing-component mapping.
license: MIT
compatibility: opencode, claude-code, cursor, windsurf, codex
---

# Figma XML to Multi-Platform UI (1:1 Implementation Rules)

Converting exported Figma XML into code is a translation job, not a redesign. Every node, string, dimension, and color in the XML must exist in the output. Never invent layout, never approximate values, never skip a node.

Follow this 5-step pipeline.

## Step 1: Detect Target Platform and Load Only That Reference

Inspect the workspace (or the user's explicit instruction) to identify the platform, then read **only** the matching reference file before writing any code:

| Signal | Reference |
|---|---|
| `react-native` in `package.json`, `.tsx` screens under `app/` with `View`/`Text` | `references/react-native.md` |
| `react` / `next` / `vite` in `package.json`, `app/`, `pages/`, `src/` web entry | `references/web-react.md` |
| `.xcodeproj`, `.xcworkspace`, `Package.swift`, or `.swift` files present | `references/swiftui.md` |

If two platforms match, ask which one before generating. Do not load all three references — that burns context and mixes conventions.

## Step 2: Load Project Overrides and Discover Design Tokens

1. **Overrides first.** If `.opencode/figma-map.md` exists at the workspace root, read it before anything else. Its component, token, and icon mappings outrank every heuristic below. If it does not exist, do not block on it — mention `assets/figma-map.template.md` once the task is done.
2. **Scan existing theme sources.**
   - JS/TS: `tailwind.config.*`, `globals.css`, `variables.css`, `theme.ts`, `tokens.ts`, `constants/Colors.ts`.
   - SwiftUI: `Assets.xcassets` (`.colorset`), `Colors.swift`, `Theme.swift`, `DesignTokens.swift`.
3. **1:1 token rule.** Map a value to an existing token only when the value matches exactly, or when `figma-map.md` names that semantic token explicitly. Otherwise emit the raw hex/RGBA and numeric value. Optionally note the raw value once so the user can promote it to a token later — but never substitute an "almost equal" token.

## Step 3: Reuse Existing Components and Map Vector Icons

1. **Component reuse.** Scan `src/components/`, `components/ui/`, or the Swift `Views/Components/` folder. When an XML `<instance name="...">` or a semantic `<frame name="...">` matches an existing component, inspect that component's props or initializer, pull the text/icon/variant values out of the XML children, and render the component. Never rebuild its internals.
2. **Inner structure of reused components is not translated.** If the XML shows a child that the component already renders (leading icon, chevron, loading state), do not emit it again.
3. **Icon detection.** Treat any `<vector>`, `<boolean-operation>`, or `<instance>` named `icon-*`, `ic_*`, `Icon/*`, or any square vector container `<= 32x32` as an icon. Apply the icon rules in the loaded reference file.
4. **Custom art.** For brand logos, illustrations, and multi-path vectors with no library equivalent, keep the exact `width` x `height` bounds and leave a `TODO: export asset "<name>"` comment. Do not fake them with a generic icon.

## Step 4: Audit the Whole Tree, Then Generate 1:1 Code

- Read the entire XML file before writing code so no `<frame>`, `<group>`, `<text>`, `<rectangle>`, or `<vector>` node is skipped or invented.
- Preserve exact numbers: width, height, padding, `itemSpacing`, corner radii, border widths, hex/RGBA colors, opacity, `fontSize`, `fontWeight`, `lineHeight`, `letterSpacing`.
- Preserve source order of siblings. Absolute-positioned children (no `layoutMode`) need explicit `left`/`top` or offsets, not guessed flex order.
- Map interactive node names (`Button`, `Btn`, `Input`, `TextField`, `Tab`, `CardPressable`) to interactive primitives per the loaded reference.
- Text content comes from the XML verbatim, including punctuation and casing. Never rewrite copy.

## Step 5: Final 1:1 Parity and Import Check

Before reporting done, verify:

1. Every XML node and every text string appears in the generated code — walk the tree top to bottom and tick each one off.
2. Every imported component, icon, and token resolves to a real path or export in this repo.
3. No dimension, gap, radius, or color was rounded or approximated.
4. The file compiles under the project's own lint/type conventions (imports sorted as the repo does, no unused imports).

## Reference Files

- `references/react-native.md` — RN primitives, Flexbox mapping, StyleSheet vs NativeWind, shadows, icons.
- `references/web-react.md` — React/Vite/Next, Tailwind vs CSS Modules, semantic HTML, box-shadow, icons.
- `references/swiftui.md` — HStack/VStack/ZStack, modifier ordering, SF Symbols, hex color fallback.

## Assets

- `assets/figma-map.template.md` — starter `.opencode/figma-map.md` for custom components, tokens, and icon libraries.
- `examples/sample-login.xml` — a complete login screen in FigML format, useful as a smoke test: run the pipeline against it and compare the output to the visual description in the file's header comment.
