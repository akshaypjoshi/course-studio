#!/usr/bin/env python3
"""Scaffold a course workspace and wire it to the Anatomy skill.

    python3 workspace.py init <courses-dir> [--anatomy <path-to-anatomy-skill>]
        Copies Anatomy's kit/ and scripts/ into <courses-dir>/_anatomy/ so every
        figure builds from one pinned copy (and keeps building on any machine).

    python3 workspace.py course <courses-dir> <slug>
        Creates <courses-dir>/<slug>/course.json from the template (if missing).

    python3 workspace.py chapter <course-dir> <n>
        Creates chapters/<nn-slug>/chapter.md for chapter n of course.json, pre-filled
        with its title, summary, outcomes and one ::figure slot per planned figure,
        plus figures/<id>/brief.md for each planned figure.

    python3 workspace.py figure <chapter-dir> <fig-id>
        Creates figures/<fig-id>/brief.md and a build.mjs stub that imports the
        vendored kit with the right relative path.
"""
import json
import os
import re
import shutil
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
TEMPLATES = SKILL / "assets" / "templates"


def find_anatomy(explicit=None) -> Path:
    cands = [explicit] if explicit else []
    cands += [os.environ.get("ANATOMY_SKILL")]
    home = Path.home()
    cands += [home / ".claude/skills/anatomy", home / ".agents/skills/anatomy", home / ".config/opencode/skills/anatomy"]
    mnt = Path("/mnt/skills")
    if mnt.exists():  # the user's own copy first, then the rest
        cands += [mnt / "user/anatomy"] + sorted(p for p in mnt.glob("*/anatomy") if p.parent.name != "user")
    cands += sorted(home.glob(".claude/skills/**/anatomy"))
    cands += sorted(home.glob(".claude/plugins/**/anatomy"))  # installed as a Claude Code plugin
    cands += sorted(SKILL.parent.glob("*anatomy*"))
    found = []
    for c in cands:
        if c and (Path(c) / "kit" / "iso-kit.mjs").exists() and Path(c).resolve() not in [f.resolve() for f in found]:
            found.append(Path(c))
    if not found:
        sys.exit("Could not find the Anatomy skill (a folder with kit/iso-kit.mjs). Pass --anatomy <path> or set ANATOMY_SKILL.")
    if len(found) > 1 and not explicit:
        print(f"note: {len(found)} copies of Anatomy found; using {found[0]} (pass --anatomy to choose)")
    return found[0]


def init(courses: Path, explicit=None):
    a = find_anatomy(explicit)
    dst = courses / "_anatomy"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(a / "kit", dst / "kit")
    (dst / "scripts").mkdir(parents=True)
    for f in (a / "scripts").glob("*.mjs"):
        if not f.name.endswith(".test.mjs"):
            shutil.copy2(f, dst / "scripts" / f.name)
    shutil.copy2(a / "SKILL.md", dst / "SKILL.md")
    if (a / "references").is_dir():
        shutil.copytree(a / "references", dst / "references")
    ex = a / "examples" / "dial-indicator"  # the smallest example, for orientation; open the rest in the skill itself
    if ex.is_dir():
        shutil.copytree(ex, dst / "examples" / "dial-indicator", ignore=shutil.ignore_patterns("*.html", "shots"))
    (dst / "SOURCE.txt").write_text(f"Copied from {a}\nOther examples: {a / 'examples'}\nRe-run `workspace.py init` to update.\n")
    print(f"vendored Anatomy from {a} → {dst}")


def course(courses: Path, slug: str):
    d = courses / slug
    d.mkdir(parents=True, exist_ok=True)
    cj = d / "course.json"
    if cj.exists():
        print(f"{cj} exists, left as is")
        return
    t = json.loads((TEMPLATES / "course.json").read_text())
    t["slug"] = slug
    cj.write_text(json.dumps(t, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {cj}")


def chapter_dirname(ch):
    return ch.get("dir") or f'{int(ch["n"]):02d}-{ch["slug"]}'


def brief(chapter_dir: Path, fid: str, plan=None):
    fd = chapter_dir / "figures" / fid
    fd.mkdir(parents=True, exist_ok=True)
    b = fd / "brief.md"
    if not b.exists():
        text = (TEMPLATES / "brief.md").read_text()
        plan = plan or {}
        text = text.replace("{{id}}", fid).replace("{{concept}}", plan.get("concept", "")) \
                   .replace("{{object}}", plan.get("object", "")).replace("{{size}}", plan.get("size", "Figure"))
        b.write_text(text)
    stub = fd / "build.mjs"
    if not stub.exists():
        # find courses root (the folder holding _anatomy) to compute the import path
        root = next((p for p in fd.parents if (p / "_anatomy").exists()), None)
        rel = os.path.relpath(root / "_anatomy", fd).replace(os.sep, "/") if root else "../../../../../_anatomy"
        stub.write_text((TEMPLATES / "build.mjs").read_text().replace("{{ANATOMY}}", rel).replace("{{id}}", fid))
    print(f"figure scaffold: {fd}")


def chapter(course_dir: Path, n: int):
    c = json.loads((course_dir / "course.json").read_text())
    ch = next((x for x in c.get("chapters", []) if int(x["n"]) == n), None)
    if not ch:
        sys.exit(f"chapter {n} not in course.json")
    d = course_dir / "chapters" / chapter_dirname(ch)
    d.mkdir(parents=True, exist_ok=True)
    md = d / "chapter.md"
    if not md.exists():
        outcomes = "\n".join(f"  - {o}" for o in ch.get("outcomes", [])) or "  - "
        figs = "\n\n".join(f"::figure {f['id']}" for f in ch.get("figures", []))
        md.write_text(f"""---
title: {ch['title']}
dek: {ch.get('summary', '')}
chapter: {n}
minutes: {ch.get('minutes', '')}
level: {ch.get('level', '')}
glyph: {ch.get('glyph', '')}
outcomes:
{outcomes}
---

<!-- Outline first (see references/writing.md), then write each section. -->

## The one idea

{figs}
""")
        print(f"wrote {md}")
    for f in ch.get("figures", []):
        brief(d, f["id"], f)


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    explicit = None
    if "--anatomy" in a:
        i = a.index("--anatomy"); explicit = a[i + 1]; del a[i:i + 2]
    cmd = a[0]
    if cmd == "init" and len(a) == 2:
        init(Path(a[1]).resolve(), explicit)
    elif cmd == "course" and len(a) == 3:
        course(Path(a[1]).resolve(), a[2])
    elif cmd == "chapter" and len(a) == 3:
        chapter(Path(a[1]).resolve(), int(a[2]))
    elif cmd == "figure" and len(a) == 3:
        if not re.match(r"^[\w\-]+$", a[2]):
            sys.exit("figure ids are letters, digits, - and _")
        brief(Path(a[1]).resolve(), a[2])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
