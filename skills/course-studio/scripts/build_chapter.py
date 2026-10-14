#!/usr/bin/env python3
"""Build a chapter (or a notes page) from Markdown into a styled HTML page that
embeds its Anatomy figures.

Usage:
    python3 build_chapter.py <chapter.md> [out.html]

Default output: <chapter dir>/../../dist/<chapter-dir-name>.html when the chapter
lives in courses/<slug>/chapters/<nn-slug>/, else next to the Markdown.

Markdown conventions (see references/writing.md §5):
  front matter   --- yaml ---  (title, dek, chapter, minutes, level, glyph, outcomes, kind)
  ## headings    numbered automatically, listed in the table of contents
  > [!INTUITION] / [!PITFALL] / [!INTERVIEW] / [!KEY] / [!TRADEOFF]   callouts
  > [!CHECK] Question text   (body = answer)   collapsible self-check
  > [!RECAP]                                   dark recap block
  ::figure <fig-id> | caption                  an Anatomy figure from figures/<fig-id>/
"""
import base64
import gzip
import json
import re
import sys
from pathlib import Path

import markdown
import yaml
from pygments.formatters import HtmlFormatter

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _pages import accent_vars, esc, find_course_json, load_course, page, FALLBACK  # noqa: E402

CALLOUT_LABELS = {
    "INTUITION": "Intuition", "PITFALL": "Pitfall", "INTERVIEW": "In the interview",
    "KEY": "Key idea", "NOTE": "Note", "TRADEOFF": "Trade-off", "RECAP": "Recap",
}
MD_EXT = ["tables", "fenced_code", "codehilite", "sane_lists", "attr_list", "md_in_html", "smarty"]
MD_CFG = {"codehilite": {"guess_lang": False, "css_class": "codehilite"}}


def md(text: str) -> str:
    return markdown.markdown(text, extensions=MD_EXT, extension_configs=MD_CFG)


def split_front(src: str):
    m = re.match(r"\s*---\s*\n(.*?)\n---\s*\n", src, re.S)
    if not m:
        return {}, src
    return yaml.safe_load(m.group(1)) or {}, src[m.end():]


def find_figure(fig_dir: Path):
    """Return (dark_html, light_html) paths for an Anatomy figure folder, or (None, None)."""
    if not fig_dir.is_dir():
        return None, None
    pages = sorted(p for p in fig_dir.glob("*.html") if not p.name.startswith("_"))
    light = next((p for p in pages if p.stem.endswith("-light")), None)
    dark = next((p for p in pages if not p.stem.endswith("-light")), None)
    return dark or light, light or dark


# The frame's color-scheme must match the figure's root, or Chrome paints an opaque canvas behind it.
IFRAME_FIX = ("<style>html{color-scheme:__T__!important}html,body{background:transparent!important;margin:0!important}.iso-page{margin:6px auto 4px!important}</style>"
              "<script>window.__errs=[];addEventListener('error',function(e){__errs.push(String(e.message))});</script>")


def figure_dir(fid: str, base: Path) -> Path:
    """figures/<id>/ next to the chapter, else in any other chapter of the same course (for reuse in notes)."""
    local = base / "figures" / fid
    if local.is_dir():
        return local
    for root in [base.parent, base.parent.parent]:
        for d in sorted(root.glob(f"*/figures/{fid}")) + sorted(root.glob(f"chapters/*/figures/{fid}")):
            if d.is_dir():
                return d
    return local


def figure_html(fid: str, caption: str, n: int, base: Path, figures: list) -> str:
    fdir = figure_dir(fid, base)
    dark, light = find_figure(fdir)
    # the Anatomy card already carries "Fig n", a title and its own caption; ours is an optional lead-in
    cap = f'<figcaption>{md(caption)[3:-4]}</figcaption>' if caption else ""
    if not dark:
        brief = fdir / "brief.md"
        what = ""
        if brief.exists():
            first = [l for l in brief.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
            what = esc(first[0][:220]) if first else ""
        figures.append({"id": fid, "status": "pending"})
        return (f'<div class="figure pending" data-fig="{esc(fid)}"><span class="fig-no">Fig {n} · pending</span>'
                f'<p><b>{esc(fid)}</b>{" — " + what if what else ""}</p>'
                f'{"<p>" + esc(caption) + "</p>" if caption else ""}</div>')
    figures.append({"id": fid, "status": "built", "dark": dark.name, "light": light.name})
    # both themes are embedded; the page script picks one and sizes the frame to its content
    # gzip+base64: small, and keeps the figure's markup and scripts away from the chapter's parser.
    # Anatomy's two theme pages usually differ only in data-theme, so one copy serves both.
    d_txt, l_txt = dark.read_text(encoding="utf-8"), light.read_text(encoding="utf-8")
    pack = lambda t: base64.b64encode(gzip.compress(t.encode(), 9)).decode()
    if l_txt.replace('data-theme="light"', 'data-theme="dark"') == d_txt:
        attrs = f'data-one="{pack(d_txt)}"'
    else:
        attrs = f'data-dark="{pack(d_txt)}" data-light="{pack(l_txt)}"'
    return (f'<figure class="figure" data-fig="{esc(fid)}" {attrs}>'
            f'<iframe title="Figure {n}: {esc(fid)}" scrolling="no"></iframe>'
            f"{cap}</figure>")


FIG_SCRIPT = r"""
(function(){
  var FIX = __FIX__;
  function theme(){ var t=document.documentElement.dataset.theme; if(t) return t;
    return matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'; }
  function size(f){ try{ var d=f.contentDocument; if(!d||!d.body) return;
    f.style.height = Math.max(d.documentElement.scrollHeight, d.body.scrollHeight) + 'px'; }catch(e){} }
  function load(fig){
    var t=theme(); if(fig.dataset.loaded===t) return; fig.dataset.loaded=t;
    var f=fig.querySelector('iframe'), one=fig.getAttribute('data-one');
    var b=atob(one || fig.getAttribute('data-'+t)), bytes=Uint8Array.from(b, function(c){return c.charCodeAt(0)});
    f.style.colorScheme = t;
    new Response(new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'))).text().then(function(html){
      if (one && t==='light') html = html.split('data-theme="dark"').join('data-theme="light"');
      html = html.replace('</head>', FIX.split('__T__').join(t) + '</head>');
      f.srcdoc = html;
    });
    f.onload=function(){ size(f); setTimeout(function(){size(f)},300); setTimeout(function(){size(f)},1200);
      try{ new ResizeObserver(function(){size(f)}).observe(f.contentDocument.body); }catch(e){} };
  }
  var figs=[].slice.call(document.querySelectorAll('figure.figure'));
  var io = 'IntersectionObserver' in window ? new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ load(e.target); io.unobserve(e.target);} }); }, {rootMargin:'600px'}) : null;
  figs.forEach(function(f){ io ? io.observe(f) : load(f); });
  matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(){ figs.forEach(function(f){ if(f.dataset.loaded) load(f); }); });
  addEventListener('resize', function(){ figs.forEach(function(f){ var i=f.querySelector('iframe'); if(f.dataset.loaded) size(i); }); });
})();
"""


def preprocess(body: str, base: Path, figures: list):
    """Turn callouts and ::figure lines into HTML blocks before Markdown runs."""
    out, lines, i, n_fig = [], body.split("\n"), 0, 0
    in_fence = False
    while i < len(lines):
        line = lines[i]
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        if in_fence:
            out.append(line); i += 1; continue
        fm = re.match(r"^::figure\s+([\w\-]+)\s*(?:\|\s*(.*))?$", line.strip())
        if fm:
            n_fig += 1
            out.append("")
            out.append(figure_html(fm.group(1), (fm.group(2) or "").strip(), n_fig, base, figures))
            out.append("")
            i += 1
            continue
        cm = re.match(r"^>\s*\[!(\w+)\]\s*(.*)$", line)
        if cm:
            kind, title = cm.group(1).upper(), cm.group(2).strip()
            block = []
            i += 1
            while i < len(lines) and lines[i].startswith(">"):
                block.append(re.sub(r"^>\s?", "", lines[i]))
                i += 1
            inner = md("\n".join(block))
            if kind == "CHECK":
                q = md(title)[3:-4] if title else "Check yourself"
                out.append(f'\n<details class="check"><summary><span>{q}</span></summary><div>{inner}</div></details>\n')
            elif kind == "RECAP":
                out.append(f'\n<div class="recap"><span class="label">{esc(title or "Recap")}</span>{inner}</div>\n')
            else:
                label = title or CALLOUT_LABELS.get(kind, kind.title())
                out.append(f'\n<div class="callout {kind.lower()}"><span class="label">{esc(label)}</span>{inner}</div>\n')
            continue
        out.append(line)
        i += 1
    return "\n".join(out)


def number_headings(html_body: str):
    toc, n = [], 0

    def rep(m):
        nonlocal n
        attrs, text = m.group(1) or "", m.group(2)
        if 'class="nonum"' in attrs:
            return m.group(0)
        n += 1
        plain = re.sub(r"<[^>]+>", "", text)
        idm = re.search(r'id="([^"]+)"', attrs)
        hid = idm.group(1) if idm else re.sub(r"[^a-z0-9]+", "-", plain.lower()).strip("-")
        toc.append((hid, plain))
        return f'<h2 id="{hid}"><span class="num">{n:02d}</span>{text}</h2>'

    return re.sub(r"<h2([^>]*)>(.*?)</h2>", rep, html_body), toc


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src_path = Path(sys.argv[1]).resolve()
    base = src_path.parent
    fm, body = split_front(src_path.read_text(encoding="utf-8"))

    cj = find_course_json(base)
    course = load_course(cj) if cj else dict(FALLBACK, title=fm.get("course", ""), code=fm.get("glyph", ""))
    if cj and len(sys.argv) < 3:
        out = cj.parent / "dist" / f"{base.name}.html"
    else:
        out = Path(sys.argv[2]) if len(sys.argv) > 2 else base / f"{src_path.stem}.html"
    out.parent.mkdir(parents=True, exist_ok=True)

    figures = []
    html_body, toc = number_headings(md(preprocess(body, base, figures)))

    kind = fm.get("kind", "chapter")  # chapter | notes | cheatsheet
    ch = fm.get("chapter")
    pills = []
    if ch is not None:
        pills.append(f'<span class="pill dark">{"Ch " + str(ch).zfill(2) if str(ch).isdigit() else esc(ch)}</span>')
    elif kind != "chapter":
        pills.append(f'<span class="pill dark">{esc(kind)}</span>')
    if course.get("title"):
        pills.append(f'<span class="pill">{esc(course["title"])}</span>')
    meta = " · ".join(x for x in [fm.get("level"), f'{fm["minutes"]} min' if fm.get("minutes") else None,
                                   f'{len(figures)} fig' if figures else None] if x)
    glyph = fm.get("glyph") or course.get("code", "")
    hero = f"""<header class="hero"><div class="badges">{''.join(pills)}</div><div class="meta">{esc(meta)}</div>
<h1>{esc(fm.get('title', src_path.stem))}</h1><p class="dek">{esc(fm.get('dek', ''))}</p>
<div class="glyph" aria-hidden="true">{esc(glyph)}</div></header>"""

    crumbs = ""
    if cj:
        crumbs = (f'<nav class="crumbs"><a href="index.html">{esc(course.get("title", "Course"))}</a>'
                  f'<span>/</span><span>{esc(fm.get("title", ""))}</span></nav>')

    outcomes = ""
    if fm.get("outcomes"):
        outcomes = '<section class="outcomes"><b>After this you can</b><ul>' + "".join(
            f"<li>{md(str(o))[3:-4]}</li>" for o in fm["outcomes"]) + "</ul></section>"
    toc_html = ""
    if len(toc) >= 4:
        toc_html = '<nav class="toc"><b>In this chapter</b><ol>' + "".join(
            f'<li><a href="#{h}">{esc(t)}</a></li>' for h, t in toc) + "</ol></nav>"

    pager = ""
    if cj:
        chapters = json.loads(cj.read_text(encoding="utf-8")).get("chapters", [])
        # only chapters that exist on disk get links, so planned chapters never produce dead links
        chapters = [c for c in chapters if (cj.parent / "chapters" / (c.get("dir") or f'{int(c["n"]):02d}-{c["slug"]}')).joinpath("chapter.md").exists()]
        slugs = [c.get("dir") or f'{int(c["n"]):02d}-{c["slug"]}' for c in chapters]
        if base.name in slugs:
            k = slugs.index(base.name)
            prev_ = chapters[k - 1] if k > 0 else None
            next_ = chapters[k + 1] if k + 1 < len(chapters) else None
            a = lambda c, s, lab, cls="": (f'<a class="{cls}" href="{s}.html"><span>{lab}</span>{esc(c["title"])}</a>' if c else "<span></span>")
            pager = f'<nav class="pager">{a(prev_, slugs[k-1] if prev_ else "", "← Previous")}{a(next_, slugs[k+1] if next_ else "", "Next →", "next")}</nav>'
            pager = pager.replace('class="next"', 'class="next" style="text-align:right;margin-left:auto"')

    dark_fmt = HtmlFormatter(style="github-dark")
    code_css = (HtmlFormatter(style="default").get_style_defs(".codehilite")
                + "\n" + dark_fmt.get_style_defs(":root[data-theme=dark] .codehilite")
                + "\n@media (prefers-color-scheme: dark){\n"
                + dark_fmt.get_style_defs(":root:not([data-theme=light]) .codehilite") + "\n}"
                + "\n.codehilite,.codehilite pre{background:var(--code-bg)!important}")

    fig_script = FIG_SCRIPT.replace("__FIX__", json.dumps(IFRAME_FIX).replace("</", "<\\/"))
    body_html = f'<main class="page">{crumbs}{hero}{outcomes}{toc_html}<article class="prose">{html_body}</article>{pager}</main>'
    out.write_text(page(fm.get("title", "Chapter"), body_html, accent_vars(course), code_css,
                        fig_script if any(f["status"] == "built" for f in figures) else ""), encoding="utf-8")
    built = sum(f["status"] == "built" for f in figures)
    pending = [f["id"] for f in figures if f["status"] == "pending"]
    print(f"wrote {out} — {len(toc)} sections, {built} figures embedded"
          + (f", pending: {', '.join(pending)}" if pending else ""))


if __name__ == "__main__":
    main()
