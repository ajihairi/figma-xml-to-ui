# Publishing and verification

Exact steps for keeping the public repo discoverable. Replace the owner path if it ever moves.

Repo: `https://github.com/ajihairi/figma-xml-to-ui`
Canonical install: `npx skills add ajihairi/figma-xml-to-ui`

Current state (verified): public repository, `main` is the default branch, 6 topics applied, `npx skills add … --list` resolves one skill.

---

## 1. Topics (helps skills.sh / GitHub discovery)

Six topics are intended for this repo: `agent-skills`, `opencode`, `claude-code`, `figma`, `swiftui`, `react-native`.

### Option A — GitHub web UI (no tooling)

1. Open <https://github.com/ajihairi/figma-xml-to-ui>.
2. In the right sidebar next to **About**, click the gear icon.
3. In **Topics**, type `agent-skills` and press Enter. Repeat for each:
   `opencode`, `claude-code`, `figma`, `swiftui`, `react-native`.
4. Click **Save changes**.

### Option B — GitHub CLI

```bash
gh auth login                       # once per machine
gh repo edit ajihairi/figma-xml-to-ui \
  --add-topic agent-skills \
  --add-topic opencode \
  --add-topic claude-code \
  --add-topic figma \
  --add-topic swiftui \
  --add-topic react-native
```

Verify:

```bash
gh repo view ajihairi/figma-xml-to-ui --json repositoryTopics \
  -q '.repositoryTopics[].name'
```

### Option C — REST API

Requires a token with `public_repo` (or fine-grained "Administration" write).

```bash
export GITHUB_TOKEN=ghp_xxx
curl -sS -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  https://api.github.com/repos/ajihairi/figma-xml-to-ui/topics \
  -d '{"names":["agent-skills","opencode","claude-code","figma","swiftui","react-native"]}'
```

Rules: lowercase, hyphens instead of spaces, max 20 topics.

### Troubleshooting: `api.github.com` won't resolve

Some VPN / corporate resolvers fail on `api.github.com` while `github.com` still works. `gh` has no per-host DNS flag, so use `curl` with a pinned IP:

```bash
IP=$(dig +short api.github.com @1.1.1.1 | tail -1)
curl -sS --resolve "api.github.com:443:$IP" \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  https://api.github.com/repos/ajihairi/figma-xml-to-ui/topics
```

Verify without auth (a public repo returns the list):

```bash
curl -sS --resolve "api.github.com:443:$IP" \
  https://api.github.com/repos/ajihairi/figma-xml-to-ui/topics
```

---

## 2. Verify the skill is installable

Run in any empty directory (not inside this repo):

```bash
npx skills add ajihairi/figma-xml-to-ui --list
```

Expected output:

```
◇  Found 1 skill
   figma-xml-to-ui
   Use when converting an exported Figma XML file ...
```

If it reports `Found 0 skills`, the frontmatter failed to parse — check `name` and `description` exist and that the file is at `skills/figma-xml-to-ui/SKILL.md`.

Confirm the repo is public without credentials:

```bash
git -c credential.helper= ls-remote https://github.com/ajihairi/figma-xml-to-ui
```

A commit hash means anonymous access works. A `403` / auth prompt means the repo is still private.

---

## 3. skills.sh indexing

Listings are generated from repository crawls and install traffic; there is no manual submit form. After the first few installs, check:

```bash
curl -s "https://skills.sh/api/search?q=figma-xml-to-ui"
```

Empty `skills: []` right after publishing is expected. Topics from step 1 improve crawl matching. If it is still absent after a week, open an issue at <https://github.com/vercel-labs/skills/issues> with the repo URL.

---

## 4. Regenerate the preview render

`examples/preview.html` is the hand-checked 1:1 render of `examples/sample-login.xml`. After changing either file, regenerate the PNG:

```bash
cd figma-xml-to-ui
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --hide-scrollbars \
  --window-size=375,812 --force-device-scale-factor=2 \
  --default-background-color=ffffff \
  --screenshot=examples/preview.png \
  "file://$PWD/examples/preview.html"
```

On Linux use `google-chrome` or `chromium` instead of the macOS app path. Output is 750 × 1624 (375 × 812 at 2×).

Then compare generated UI against the PNG at 100%, not by eyeballing a screenshot inside a device simulator with its own chrome.

---

## 5. Pre-push checklist

- [ ] `xmllint --noout examples/sample-login.xml`
- [ ] `npx skills add ajihairi/figma-xml-to-ui --list` finds exactly one skill
- [ ] No client XML, `.env`, or proprietary tokens under `examples/`
- [ ] `LICENSE` copyright line and commit author are the intended handle
- [ ] Topics set (step 1)
- [ ] `examples/preview.png` regenerated if the XML changed
