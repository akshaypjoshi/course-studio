#!/usr/bin/env bash
# Re-vendor the Anatomy engine (MIT, https://github.com/wheresryan22/anatomy) into
# skills/course-studio/anatomy/ so Course Studio installs as a single skill.
#   tools/update-anatomy.sh [git-ref]      (default: main)
# Keeps: kit/, scripts/ (no tests), references/, examples/ (sources only), LICENSE.
# Drops: the community-gallery publisher (publish.mjs / publish.md), tests, evals,
# built example pages. SKILL.md becomes ANATOMY.md so it isn't installed as a second skill.
set -euo pipefail
REF="${1:-main}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DST="$ROOT/skills/course-studio/anatomy"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

git clone -q https://github.com/wheresryan22/anatomy "$TMP/src"
git -C "$TMP/src" checkout -q "$REF"
SHA="$(git -C "$TMP/src" rev-parse HEAD)"
VER="$(git -C "$TMP/src" describe --tags --always)"

rm -rf "$DST"; mkdir -p "$DST/scripts"
cp -R "$TMP/src/kit" "$TMP/src/references" "$DST/"
cp "$TMP/src/LICENSE" "$DST/LICENSE"
for f in "$TMP/src"/scripts/*.mjs; do
  case "$f" in *.test.mjs|*/publish.mjs) ;; *) cp "$f" "$DST/scripts/";; esac
done
rm -f "$DST/references/publish.md"
(cd "$TMP/src" && find examples -type f ! -name '*.html' ! -name '*.png' ! -name '*.webp' -print0 | xargs -0 -I{} rsync -R {} "$DST/")

python3 - "$TMP/src/SKILL.md" "$DST/ANATOMY.md" "$VER" "$SHA" <<'PY'
import re, sys
src, dst, ver, sha = sys.argv[1:]
s = open(src).read()
s = re.sub(r"\A---\n.*?\n---\n", "", s, flags=re.S)                     # no frontmatter: not a separate skill
s = "\n".join(l for l in s.splitlines() if "references/publish.md" not in l) + "\n"
s = s.replace("This skill makes figures", "Anatomy makes figures").replace("ship with the skill", "ship in this folder")
head = (f"<!-- Bundled Anatomy engine {ver} ({sha[:7]}), MIT, (c) Ryan — https://github.com/wheresryan22/anatomy\n"
        f"     Vendored by tools/update-anatomy.sh; edit there, not here. Gallery publishing is not included. -->\n\n"
        "> **Inside Course Studio:** every path below (`kit/`, `scripts/`, `references/`, `examples/`) is relative to this\n"
        "> `anatomy/` folder. Course figures import the copy vendored into the workspace (`<courses>/_anatomy/`) by\n"
        "> `workspace.py init`; follow course-studio's `references/figures.md` for the output contract.\n\n")
open(dst, "w").write(head + s)
PY
printf 'Anatomy %s\ncommit %s\nsource https://github.com/wheresryan22/anatomy\nlicense MIT (see LICENSE in this folder)\n' "$VER" "$SHA" > "$DST/VERSION"
echo "vendored Anatomy $VER ($SHA) → $DST"
du -sh "$DST"
