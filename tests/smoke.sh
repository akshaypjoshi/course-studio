#!/usr/bin/env bash
# Smoke test: rebuild the example course from scratch and check every page.
#   tests/smoke.sh [path-to-other-anatomy]   (default: the copy bundled in the skill)
# Needs: python deps from skills/course-studio/requirements.txt, Chromium for Playwright, Node 20.10+.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILL="$ROOT/skills/course-studio"
PY="${PYTHON:-python3}"
WS="$(mktemp -d)"
trap 'rm -rf "$WS"' EXIT

ANATOMY_ARGS=()
if [ "${1:-}" != "" ]; then ANATOMY_ARGS=(--anatomy "$1"); fi

cp -R "$SKILL/examples/courses" "$WS/courses"
"$PY" "$SKILL/scripts/workspace.py" init "$WS/courses" ${ANATOMY_ARGS[@]+"${ANATOMY_ARGS[@]}"}

for fig in "$WS"/courses/*/chapters/*/figures/*/; do
  (cd "$fig" && node build.mjs && node build.mjs --audit)
done

"$PY" "$SKILL/scripts/build_course.py" "$WS/courses" --catalog
"$PY" "$SKILL/scripts/check_pages.py" "$WS/courses/dsa/dist" "${SHOTS:-$WS/shots}"
"$PY" "$SKILL/scripts/check_pages.py" "$WS/courses/dsa/dist" "${SHOTS:-$WS/shots}-mobile-dark" --mobile --dark

# scaffolds work on a fresh course
"$PY" "$SKILL/scripts/workspace.py" course "$WS/courses" smoke
"$PY" - "$WS/courses/smoke/course.json" <<'PY'
import json, sys
p = sys.argv[1]; c = json.load(open(p))
c.update(title="Smoke", code="SMK")
c["chapters"][0].update(slug="intro", title="Intro", figures=[{"id": "fig-01-idea", "concept": "x", "object": "y", "size": "Figure"}])
json.dump(c, open(p, "w"))
PY
"$PY" "$SKILL/scripts/workspace.py" chapter "$WS/courses/smoke" 1
test -f "$WS/courses/smoke/chapters/01-intro/figures/fig-01-idea/brief.md"
test -f "$WS/courses/smoke/chapters/01-intro/figures/fig-01-idea/build.mjs"
"$PY" "$SKILL/scripts/build_course.py" "$WS/courses/smoke"
grep -q 'figure pending' "$WS/courses/smoke/dist/01-intro.html"

# em dashes are caught: build warns, check reports
printf '\nIt works \xe2\x80\x94 mostly.\n' >> "$WS/courses/smoke/chapters/01-intro/chapter.md"
"$PY" "$SKILL/scripts/build_chapter.py" "$WS/courses/smoke/chapters/01-intro/chapter.md" | grep -q "WARNING: em dash"
OUT="$("$PY" "$SKILL/scripts/check_pages.py" "$WS/courses/smoke/dist/01-intro.html" "$WS/shots-dash" || true)"  # exits 1 on problems, as intended
grep -q "em dash in page" <<<"$OUT" || { echo "check_pages missed an em dash"; exit 1; }

echo "smoke test passed"
