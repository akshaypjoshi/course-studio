#!/usr/bin/env python3
"""Check built course pages in a headless browser and save screenshots.

Usage:
    python3 check_pages.py <page.html | dist-dir> [shots-dir] [--mobile] [--dark]

For every page: JS errors (page and figures), figures that failed to load or are
still pending, figure frames that are too short (clipped), horizontal page scroll
(naming the element), empty sections. Saves a full-page PNG and one PNG per figure.
Exit 1 on any problem. Then open the PNGs: the review is yours, not the script's.

Needs: pip install playwright && playwright install chromium
"""
import sys
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:  # pragma: no cover
    sys.exit("check_pages.py needs: pip install playwright && playwright install chromium")

OVERFLOW_JS = """() => { const W = document.documentElement.clientWidth, out = [];
  document.querySelectorAll('main *').forEach(el => {
    if (el.closest('pre') || el.closest('table') || el.closest('iframe')) return;
    const r = el.getBoundingClientRect();
    if (r.right > W + 1 && r.width > 0) out.push(el.tagName.toLowerCase() + (typeof el.className === 'string' && el.className ? '.' + el.className.split(' ')[0] : '') + ' "' + (el.textContent || '').trim().slice(0, 40) + '"'); });
  return out.slice(0, 5); }"""

FIGS_JS = """() => [...document.querySelectorAll('figure.figure, .figure.pending')].map(f => {
  const i = f.querySelector('iframe'); let inner = null, clipped = false;
  try { if (i && i.contentDocument && i.contentDocument.body) {
    const d = i.contentDocument; inner = Math.max(d.documentElement.scrollHeight, d.body.scrollHeight);
    clipped = inner > i.clientHeight + 4; } } catch (e) {}
  return { id: f.dataset.fig, pending: f.classList.contains('pending'), h: i ? i.clientHeight : 0, inner, clipped,
           errors: (i && i.contentWindow && i.contentWindow.__errs) || [] }; })"""



def check(page, path: Path, shots: Path, tag: str, problems: list):
    errs = []
    page.on("pageerror", lambda e: errs.append(str(e)))
    page.goto(path.as_uri())
    page.wait_for_timeout(500)
    # scroll through so lazy figures load, then let them settle
    h = page.evaluate("document.body.scrollHeight")
    for y in range(0, h + 900, 700):
        page.evaluate(f"window.scrollTo(0,{y})")
        page.wait_for_timeout(120)
    page.wait_for_timeout(1500)
    for f in page.evaluate(FIGS_JS):
        if f["pending"]:
            problems.append(f"{tag}: figure {f['id']} is pending (not built yet)")
        elif f["h"] < 120:
            problems.append(f"{tag}: figure {f['id']} did not load (frame {f['h']}px)")
        elif f["clipped"]:
            problems.append(f"{tag}: figure {f['id']} is clipped ({f['inner']}px content in {f['h']}px frame)")
        for e in f["errors"]:
            problems.append(f"{tag}: figure {f['id']} error: {e}")
    for href in page.evaluate("""() => [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href'))
        .filter(h => h && !h.startsWith('#') && !/^[a-z]+:/i.test(h))"""):
        if not (path.parent / href.split("#")[0]).exists():
            problems.append(f"{tag}: broken link → {href}")
    off = page.evaluate(OVERFLOW_JS)
    if off:
        problems.append(f"{tag}: page scrolls sideways because of " + "; ".join(off))
    empty = page.evaluate("""() => [...document.querySelectorAll('.prose h2:not(.nonum)')].filter(h => { let n = h.nextElementSibling;
        return !n || n.tagName === 'H2'; }).map(h => h.textContent)""")
    for e in empty:
        problems.append(f"{tag}: section '{e}' is empty")
    for e in errs:
        if "Failed to load resource" not in e:
            problems.append(f"{tag}: page error: {e}")
    page.evaluate("window.scrollTo(0,0)")
    page.screenshot(path=str(shots / f"{path.stem}.png"), full_page=True)
    for k, el in enumerate(page.locator("figure.figure").all()):
        el.scroll_into_view_if_needed()
        page.wait_for_timeout(600)
        el.screenshot(path=str(shots / f"{path.stem}-fig{k + 1}.png"))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    target = Path(args[0]).resolve()
    pages = sorted(target.glob("*.html")) if target.is_dir() else [target]
    mobile, dark = "--mobile" in sys.argv, "--dark" in sys.argv
    suffix = "-".join(x for x, on in (("mobile", mobile), ("dark", dark)) if on)
    default = (target if target.is_dir() else target.parent) / ("shots" + (f"-{suffix}" if suffix else ""))
    shots = Path(args[1]).resolve() if len(args) > 1 else default
    shots.mkdir(parents=True, exist_ok=True)
    problems = []
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--use-gl=swiftshader", "--enable-webgl", "--ignore-gpu-blocklist"])
        for path in pages:
            pg = b.new_page(viewport={"width": 390 if mobile else 1180, "height": 900},
                            color_scheme="dark" if dark else "light", device_scale_factor=2 if mobile else 1)
            check(pg, path, shots, path.name, problems)
            pg.close()
            print(f"  checked {path.name}")
        b.close()
    print(f"{len(pages)} pages checked, screenshots in {shots}")
    for pr in problems:
        print("PROBLEM:", pr)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
