#!/usr/bin/env python3
"""Build the Course Studio site: the landing page plus live demos built by the skill itself.

    python3 site/build.py <out-dir>

Output:
    <out>/index.html, <out>/assets/...                     landing page
    <out>/example/<course>/index.html                      each example course page (syllabus)
    <out>/example/<course>/<chapter>.html                  each written chapter, figures embedded
    <out>/example/figure/<id>[-light].html                 each figure on its own (embedded live on the landing page)
    <out>/example/index.html, <out>/example/05-hashing.html  redirects from the first site's URLs

Needs: python deps from skills/course-studio/requirements.txt (playwright not needed) and Node.js 20.10+.
The hub repo (akshaypjoshi/skills) runs this to publish skills.akshayjoshi.dev/course-studio/.
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SKILL = ROOT / "skills" / "course-studio"
ASSETS = ("figure-light.png", "figure-dark.png", "chapter-light.png", "chapter-dark.png",
          "rocket-chapter-light.png", "rocket-chapter-dark.png")
REDIRECTS = {"index.html": "dsa/index.html", "05-hashing.html": "dsa/05-hashing.html"}


def run(*cmd, cwd=None):
    print("+", " ".join(str(c) for c in cmd))
    subprocess.run([str(c) for c in cmd], cwd=cwd, check=True)


def redirect(to: str) -> str:
    return (f'<!doctype html><meta charset="utf-8"><title>Moved</title>'
            f'<link rel="canonical" href="{to}"><meta http-equiv="refresh" content="0; url={to}">'
            f'<p>Moved to <a href="{to}">{to}</a>.</p>')


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    out = Path(sys.argv[1]).resolve()
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    # landing page and its assets
    shutil.copy2(HERE / "index.html", out / "index.html")
    shutil.copytree(HERE / "assets", out / "assets")
    for name in ASSETS:
        shutil.copy2(ROOT / ".github" / "assets" / name, out / "assets" / name)

    # the live demos, built by the skill's own scripts from its bundled examples
    example, figures = out / "example", out / "example" / "figure"
    figures.mkdir(parents=True)
    with tempfile.TemporaryDirectory() as tmp:
        courses = Path(tmp) / "courses"
        shutil.copytree(SKILL / "examples" / "courses", courses)
        run(sys.executable, SKILL / "scripts" / "workspace.py", "init", courses)
        for build in sorted(courses.glob("*/chapters/*/figures/*/build.mjs")):
            run("node", "build.mjs", cwd=build.parent)
            for page in build.parent.glob("*.html"):
                shutil.copy2(page, figures / page.name)
        for course in sorted(p.parent for p in courses.glob("*/course.json")):
            run(sys.executable, SKILL / "scripts" / "build_course.py", course)
            shutil.copytree(course / "dist", example / course.name, ignore=shutil.ignore_patterns("shots*"))

    for old, new in REDIRECTS.items():
        (example / old).write_text(redirect(new), encoding="utf-8")
    print(f"site built in {out}")


if __name__ == "__main__":
    main()
