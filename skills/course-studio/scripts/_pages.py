"""Shared helpers for course-studio page builders."""
import html
import json
import sys
from pathlib import Path

try:
    import yaml  # noqa: F401
    import markdown  # noqa: F401
except ImportError:  # pragma: no cover
    sys.exit("course-studio needs: pip install markdown pyyaml pygments  (or: pip install -r requirements.txt in the skill folder)")

ASSETS = Path(__file__).resolve().parent.parent / "assets"
FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700'
    '&family=Inter+Tight:wght@700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">'
)

# Preset identities for the four built-in courses (matched by slug). course.json can override any of these.
KNOWN = {
    "dsa": {"code": "DSA", "accent": "#D04A28", "tint": "#F4E1D8", "accentDark": "#F06A45", "tintDark": "#3A2219"},
    "system-design": {"code": "SD", "accent": "#0077D6", "tint": "#D9E7EE", "accentDark": "#3B9BFF", "tintDark": "#15293A"},
    "javascript-deeply": {"code": "JS", "accent": "#9A7300", "tint": "#EDE5D2", "accentDark": "#D6A520", "tintDark": "#2E2814"},
    "low-level-design": {"code": "LLD", "accent": "#8E5BC8", "tint": "#EBE0EC", "accentDark": "#B184F0", "tintDark": "#2C2236"},
}
FALLBACK = {"accent": "#2F6F5E", "tint": "#DDEBE5", "accentDark": "#5CC4A4", "tintDark": "#18302A"}


def esc(s) -> str:
    return html.escape("" if s is None else str(s))


def load_course(path: Path) -> dict:
    c = json.loads(path.read_text(encoding="utf-8"))
    base = dict(FALLBACK)
    base.update(KNOWN.get(c.get("slug", ""), {}))
    base.update({k: v for k, v in c.items() if v is not None})
    base.setdefault("code", c.get("slug", "")[:3].upper())
    return base


def find_course_json(start: Path):
    for p in [start, *start.parents][:5]:
        f = p / "course.json"
        if f.exists():
            return f
    return None


def accent_vars(c: dict) -> str:
    return (f"--course-accent:{c['accent']};--course-tint:{c['tint']};"
            f"--course-accent-dark:{c.get('accentDark', c['accent'])};--course-tint-dark:{c.get('tintDark', c['tint'])};")


def page(title: str, body: str, style_vars: str = "", extra_css: str = "", script: str = "") -> str:
    css = (ASSETS / "notes.css").read_text(encoding="utf-8")
    return f"""<!doctype html>
<html lang="en" style="{style_vars}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
{FONTS}
<style>
{css}
{extra_css}
</style>
</head>
<body>
{body}
{f"<script>{script}</script>" if script else ""}
</body>
</html>
"""
