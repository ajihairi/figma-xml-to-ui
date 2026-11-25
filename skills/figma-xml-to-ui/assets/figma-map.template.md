# Figma Map (project overrides)

Copy this file to `.opencode/figma-map.md` at your repo root and edit the sections you care about. Rules here overrank every heuristic in the skill. Delete sections you do not use — an empty section is ignored.

## Components

Map Figma component or frame names to existing code components. FigML exports instances with the component name as the element tag, so matching is on `name` and `type="INSTANCE"`, not on the tag string. Include the props or initializer so the agent knows how to fill it.

| Figma name | Code component | Import path | Notes |
|---|---|---|---|
| `Button / Primary` | `PrimaryButton` | `@/components/ui/PrimaryButton` | props: `label`, `onPress`, `disabled`; renders its own label text |
| `Input / Text` | `TextField` | `@/components/ui/TextField` | props: `label`, `placeholder`, `value`, `onChange`; renders label above the field |
| `Card / Post` | `PostCard` | `@/components/PostCard` | props: `post`; do not emit child avatar or byline |

## Design Tokens

Map exact Figma values to semantic tokens. Only 1:1 matches — the agent will not use these for near-miss values.

### Colors

| Hex | Token | Usage |
|---|---|---|
| `#18181B` | `colors.ink` / `bg-foreground` | primary text, primary button fill |
| `#FAFAFA` | `colors.paper` / `bg-background` | page background, text on dark |
| `#71717A` | `colors.muted` / `text-muted-foreground` | secondary text |
| `#E4E4E7` | `colors.border` / `border-border` | input and divider strokes |

### Spacing

| Value | Token |
|---|---|
| `4` | `spacing.xs` |
| `8` | `spacing.sm` |
| `16` | `spacing.md` |
| `24` | `spacing.lg` |

### Radius

| Value | Token |
|---|---|
| `8` | `radius.sm` |
| `12` | `radius.md` |
| `999` | `radius.full` |

## Typography

| Figma style | Code token | Family / size / line height / weight |
|---|---|---|
| `Heading / H1` | `text.h1` | Inter 28 / 36 / 700 |
| `Body / Base` | `text.body` | Inter 15 / 22 / 400 |
| `Label / Small` | `text.caption` | Inter 13 / 18 / 600 |

## Icons

| Figma prefix | Library | Notes |
|---|---|---|
| `icon-*` | `lucide-react-native` | PascalCase the suffix |
| `brand-*` | local `@/assets/icons` | keep exact bounds, do not substitute |

## Conventions

- Language for UI copy: keep English as authored in Figma.
- File placement: screens go in `src/screens/`, shared UI in `src/components/ui/`.
- Do not introduce new dependencies for icons or fonts without asking.
- Assets: when the export has an `IMAGE` fill with no file, leave `TODO(figma): export image "<name>"` with the exact box. Never substitute a stock photo.
- Approximations: list every approximation (shadow via elevation, gradient fallback, blur) in the final report.
