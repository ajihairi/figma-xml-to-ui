# figma-xml-to-ui

An Agent Skill that turns exported Figma XML (such as **FigML**) into **1:1 UI code** for **React Native**, **React.js**, **Vite.js**, **Next.js**, and **SwiftUI** — with design-token discovery, icon mapping, and reuse of components you already have.

Built for Figma **Free / Starter** plans: no Dev Mode seat, no MCP rate limits, just an XML export and your agent.

> Maintained by **hamzhya** · repository: [`ajihairi/figma-xml-to-ui`](https://github.com/ajihairi/figma-xml-to-ui). The install command uses the GitHub owner path; `hamzhya` and `ajihairi` are the same maintainer.

---

## What it does

- **1:1 layout and visuals.** Preserves auto-layout direction, padding, gaps, `FIXED` / `HUG` / `FILL` sizing, typography, radii, hex colors, and shadows.
- **Platform routing.** Detects your stack and loads only the matching rulebook, so RN rules never leak into SwiftUI output.
- **Token discovery.** Scans `tailwind.config.*`, `globals.css`, `theme.ts`, `tokens.ts`, or Swift `Assets.xcassets` and maps values only on exact matches.
- **Component and icon reuse.** Maps XML instances to your existing components, and vector nodes to `lucide-react` / `lucide-react-native` / SF Symbols.
- **Per-project overrides.** An optional `.opencode/figma-map.md` maps Figma layer names to your codebase.

---

## Install

### One command

```bash
npx skills add ajihairi/figma-xml-to-ui
```

### Manual

Copy the skill folder into your agent's global skills directory.

**OpenCode**

```bash
mkdir -p ~/.config/opencode/skills
cp -r skills/figma-xml-to-ui ~/.config/opencode/skills/figma-xml-to-ui
```

**Claude Code**

```bash
mkdir -p ~/.claude/skills
cp -r skills/figma-xml-to-ui ~/.claude/skills/figma-xml-to-ui
```

**Cursor / Windsurf / Codex** — point the tool at `skills/figma-xml-to-ui/SKILL.md`, or copy it into the tool's own skills/rules directory.

---

## Usage

### 1. Export XML from Figma

1. Install a Figma-to-XML exporter plugin (for example [FigML](https://www.figma.com/community)) in the free Figma plan.
2. Select the frame or component you want.
3. Run **Plugins → FigML**, export, and save the file inside your project, e.g. `specs/login-screen.xml`.

### 2. Optional project overrides

```bash
mkdir -p .opencode
cp skills/figma-xml-to-ui/assets/figma-map.template.md .opencode/figma-map.md
```

Edit `.opencode/figma-map.md` to declare your components, tokens, and icon library. Rules there outrank the skill's heuristics.

### 3. Generate

```text
Use figma-xml-to-ui to convert @specs/login-screen.xml into src/screens/LoginScreen.tsx with 1:1 fidelity.
```

The agent reads the platform rulebook, discovers your tokens and components, translates the full node tree, and runs a parity check before reporting done.

---

## Try it with the bundled example

`examples/sample-login.xml` is a complete 375 × 812 login screen — nav bar, header, two inputs, primary CTA, divider, social buttons, and footer. It doubles as a smoke test: the file's header comment lists the nine expected visual results, which the agent uses as its parity checklist.

```text
Use figma-xml-to-ui to convert @examples/sample-login.xml into a single LoginScreen component. Match the 9-point checklist in the file header exactly.
```

Export it first, then diff the result against your Figma frame.

---

## Repository layout

```text
figma-xml-to-ui/
├── skills/
│   └── figma-xml-to-ui/
│       ├── SKILL.md                  # 5-step pipeline + platform router
│       ├── references/
│       │   ├── react-native.md       # RN primitives, Flexbox, NativeWind, shadows
│       │   ├── web-react.md          # React / Vite / Next, Tailwind, semantic HTML
│       │   └── swiftui.md            # HStack/VStack/ZStack, modifier order, SF Symbols
│       └── assets/
│           └── figma-map.template.md # starter .opencode/figma-map.md
├── examples/
│   └── sample-login.xml              # clean end-to-end fixture
├── LICENSE
└── README.md
```

`SKILL.md` is the only file loaded up front; the platform references and the map template load on demand, keeping context small when you only need one stack.

---

## Verify before sharing

```bash
npx skills add ajihairi/figma-xml-to-ui --list
```

Confirm the CLI lists the skill and parses the frontmatter. Also check that no client XML, `.env`, or proprietary design tokens are committed under `examples/`.

---

## License

MIT — see [LICENSE](LICENSE).
