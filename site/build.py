#!/usr/bin/env python3
"""Build the Course Studio site: the landing page plus a live demo built by the skill itself.

    python3 site/build.py <out-dir>

Output:
    <out>/index.html, <out>/assets/...          landing page
    <out>/example/index.html                    the DSA course page (syllabus)
    <out>/example/05-hashing.html               the Hashing chapter with its embedded figure
    <out>/example/figure/<id>[-light].html      the figure on its own (embedded live on the landing page)

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
FIG = "fig-01-hash-sorter"


def run(*cmd, cwd=None):
    print("+", " ".join(str(c) for c in cmd))
    subprocess.run([str(c) for c in cmd], cwd=cwd, check=True)


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
    for name in ("figure-light.png", "figure-dark.png", "chapter-light.png", "chapter-dark.png"):
        shutil.copy2(ROOT / ".github" / "assets" / name, out / "assets" / name)

    # the live demo, built by the skill's own scripts from its bundled example
    with tempfile.TemporaryDirectory() as tmp:
        courses = Path(tmp) / "courses"
        shutil.copytree(SKILL / "examples" / "courses", courses)
        run(sys.executable, SKILL / "scripts" / "workspace.py", "init", courses)
        for build in sorted(courses.glob("*/chapters/*/figures/*/build.mjs")):
            run("node", "build.mjs", cwd=build.parent)
        run(sys.executable, SKILL / "scripts" / "build_course.py", courses / "dsa")
        shutil.copytree(courses / "dsa" / "dist", out / "example", ignore=shutil.ignore_patterns("shots*"))
        fig_dir = next(courses.glob(f"dsa/chapters/*/figures/{FIG}"))
        (out / "example" / "figure").mkdir()
        for f in (f"{FIG}.html", f"{FIG}-light.html"):
            shutil.copy2(fig_dir / f, out / "example" / "figure" / f)

    print(f"site built in {out}")


if __name__ == "__main__":
    main()
