#!/usr/bin/env bash
# Regenerate examples/preview.png from examples/preview.html.
# Usage: bash scripts/preview.sh   (CHROME_BIN=/path/to/chrome to override)
set -euo pipefail

cd "$(dirname "$0")/.."

find_chrome() {
  if [ -n "${CHROME_BIN:-}" ]; then printf '%s' "$CHROME_BIN"; return; fi
  local candidates=(
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    "/Applications/Chromium.app/Contents/MacOS/Chromium"
    "google-chrome"
    "chromium"
    "chromium-browser"
  )
  local c
  for c in "${candidates[@]}"; do
    if [ -x "$c" ]; then printf '%s' "$c"; return; fi
    if command -v "$c" >/dev/null 2>&1; then command -v "$c"; return; fi
  done
}

CHROME="$(find_chrome || true)"
if [ -z "$CHROME" ]; then
  echo "error: Chrome/Chromium not found. Set CHROME_BIN=/path/to/chrome" >&2
  exit 1
fi

"$CHROME" \
  --headless=new --hide-scrollbars \
  --window-size=375,812 --force-device-scale-factor=2 \
  --default-background-color=ffffff \
  --screenshot=examples/preview.png \
  "file://$PWD/examples/preview.html"

python3 - <<'PY'
import struct
data = open("examples/preview.png", "rb").read(24)
w, h = struct.unpack(">II", data[16:24])
expected = (750, 1624)
status = "ok" if (w, h) == expected else f"UNEXPECTED (expected {expected[0]}x{expected[1]})"
print(f"wrote examples/preview.png — {w}x{h} {status}")
raise SystemExit(0 if (w, h) == expected else 1)
PY
