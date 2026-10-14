#!/usr/bin/env python3
"""Build course pages from course.json files.

Usage:
    python3 build_course.py courses/<slug>            # course page + every written chapter → courses/<slug>/dist/
    python3 build_course.py courses/ --catalog        # catalog of every course → courses/catalog.html

The course page shows the hero, outcomes and the syllabus (chapter status, minutes,
planned figures). Chapters with a chapter.md are built with build_chapter.py and linked.
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _pages import accent_vars, esc, load_course, page  # noqa: E402

HERE = Path(__file__).resolve().parent


def chapter_dir(c: dict) -> str:
    return c.get("dir") or f'{int(c["n"]):02d}-{c["slug"]}'


def price(c: dict) -> str:
    if c.get("price") in (None, ""):
        return ""
    cur = c.get("currency") or ""
    sym = {"INR": "₹", "USD": "$", "EUR": "€", "GBP": "£"}.get(cur, f"{cur} " if cur else "")
    return f"{sym}{int(c['price']):,}"


def spec_line(c: dict) -> str:
    bits = [c.get("level"), f'{c["hours"]} hrs' if c.get("hours") else None]
    if c.get("languages"):
        bits.append(" / ".join(c["languages"]))
    return " · ".join(b for b in bits if b)


def build_course(root: Path) -> Path:
    c = load_course(root / "course.json")
    dist = root / "dist"
    dist.mkdir(exist_ok=True)
    items, written = [], 0
    for ch in c.get("chapters", []):
        d = root / "chapters" / chapter_dir(ch)
        md = d / "chapter.md"
        link = None
        if md.exists():
            r = subprocess.run([sys.executable, str(HERE / "build_chapter.py"), str(md)], capture_output=True, text=True)
            print(r.stdout.strip() or r.stderr.strip())
            if r.returncode == 0:
                link = f"{chapter_dir(ch)}.html"
                written += 1
        figs = ch.get("figures", [])
        tags = [f'<span class="fig">Fig · {esc(f.get("object") or f.get("concept") or f.get("id"))}</span>' for f in figs]
        tags += [f"<span>{esc(t)}</span>" for t in ch.get("topics", [])[:6]]
        status = "" if link else f' · {esc(ch.get("status", "planned"))}'
        title = f'<a href="{link}">{esc(ch["title"])}</a>' if link else esc(ch["title"])
        items.append(f'<li><div class="n">{int(ch["n"]):02d}</div><h3>{title}</h3>'
                     f'<div class="mins">{esc(ch.get("minutes", ""))}{" min" if ch.get("minutes") else ""}{status}</div>'
                     f'<p>{esc(ch.get("summary", ""))}</p><div class="tags">{"".join(tags)}</div></li>')

    n_ch = len(c.get("chapters", []))
    meta = " · ".join(x for x in [spec_line(c), f"{n_ch} chapters" if n_ch else None] if x)
    outcomes = ""
    if c.get("outcomes"):
        outcomes = '<section class="outcomes"><b>By the end you can</b><ul>' + "".join(
            f"<li>{esc(o)}</li>" for o in c["outcomes"]) + "</ul></section>"
    prereq = ""
    if c.get("prerequisites"):
        prereq = '<section class="outcomes"><b>Before you start</b><ul>' + "".join(
            f"<li>{esc(o)}</li>" for o in c["prerequisites"]) + "</ul></section>"
    status_pill = '<span class="pill dark">Available</span>' if c.get("status") == "available" else '<span class="pill">Coming soon</span>'
    body = f"""<main class="page">
<header class="hero"><div class="badges">{status_pill}<span class="pill">{esc(price(c))}</span></div><div class="meta">{esc(meta)}</div>
<h1>{esc(c['title'])}</h1><p class="dek">{esc(c.get('tagline', ''))}</p><div class="glyph" aria-hidden="true">{esc(c['code'])}</div></header>
{outcomes}{prereq}
<article class="prose"><h2 class="nonum" style="margin-top:36px">Syllabus</h2></article>
<ol class="syllabus">{''.join(items)}</ol></main>"""
    out = dist / "index.html"
    out.write_text(page(c["title"], body, accent_vars(c)), encoding="utf-8")
    print(f"wrote {out}: {n_ch} chapters, {written} written")
    return out


def build_catalog(root: Path) -> Path:
    courses = [load_course(p) for p in sorted(root.glob("*/course.json"))]
    courses.sort(key=lambda c: (c.get("status") != "available", c.get("order", 99)))
    cards = []
    for c in courses:
        n_ch = len(c.get("chapters", [])) or c.get("chapterCount", "")
        avail = c.get("status") == "available"
        style = (f"--cl-accent:{c['accent']};--cl-tint:{c['tint']};"
                 f"--cd-accent:{c.get('accentDark', c['accent'])};--cd-tint:{c.get('tintDark', c['tint'])}")
        cards.append(f"""<a class="course-card" data-status="{'available' if avail else 'soon'}" href="{esc(c['slug'])}/dist/index.html" style="{style}">
<div class="art"><span class="pill{' dark' if avail else ''}">{'Available' if avail else 'Coming soon'}</span><span class="ch">{n_ch} ch</span>
<div class="glyph" aria-hidden="true">{esc(c['code'])}</div></div>
<div class="body"><h3>{esc(c['title'])}</h3><p>{esc(c.get('tagline', ''))}</p><div class="spec">{esc(spec_line(c))}</div>
<div class="foot"><span class="price">{esc(price(c))}</span><span class="btn{' primary' if avail else ''}">{'Start' if avail else 'Join waitlist'}</span></div></div></a>""")
    body = f"""<main class="catalog"><div class="catalog-head"><div class="filters" role="group" aria-label="Filter courses">
<button aria-pressed="true" data-f="all">All</button><button aria-pressed="false" data-f="available">Available now</button><button aria-pressed="false" data-f="soon">Coming soon</button></div>
<span class="count">{len(courses)} courses</span></div><div class="grid">{''.join(cards)}</div></main>"""
    css = """.course-card{--c-accent:var(--cl-accent);--c-tint:var(--cl-tint)}
@media (prefers-color-scheme: dark){:root:not([data-theme=light]) .course-card{--c-accent:var(--cd-accent);--c-tint:var(--cd-tint)}}
:root[data-theme=dark] .course-card{--c-accent:var(--cd-accent);--c-tint:var(--cd-tint)}"""
    js = """document.querySelectorAll('.filters button').forEach(function(b){b.onclick=function(){
document.querySelectorAll('.filters button').forEach(function(x){x.setAttribute('aria-pressed', x===b)});
var f=b.dataset.f, n=0; document.querySelectorAll('.course-card').forEach(function(c){var on=f==='all'||c.dataset.status===f; c.style.display=on?'':'none'; n+=on});
document.querySelector('.count').textContent=n+' courses';}});"""
    out = root / "catalog.html"
    out.write_text(page("Courses", body, "", css, js), encoding="utf-8")
    print(f"wrote {out}: {len(courses)} courses")
    return out


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    root = Path(sys.argv[1]).resolve()
    if "--catalog" in sys.argv:
        for cj in sorted(root.glob("*/course.json")):
            build_course(cj.parent)
        build_catalog(root)
    else:
        build_course(root)


if __name__ == "__main__":
    main()
