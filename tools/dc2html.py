#!/usr/bin/env python3
"""Convert a Design-canvas artboard (.dc.html) into a standalone page for this repo.

Usage:
    python3 tools/dc2html.py SRC.dc.html OUT.html [--rename Old.dc.html=new.html ...]
                             [--crumb "หน้าหลัก=../index.html" --crumb "Section=index.html" --crumb "This page="]

  --crumb adds a sticky top bar: the first crumb is the home button, an empty
  href marks the current page.  build.sh holds the exact commands for this repo.

What it does:
  * moves the <helmet> block (fonts, page styles) into <head>
  * wraps the <x-dc> markup in <template id="dc-template"> and adds <div id="dc-root">
  * swaps the canvas's support.js for ../shared/dc-runtime.js
  * rewrites links between artboards using the --rename map
"""
import re
import sys


HOME_ICON = ('<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
             'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
             '<path d="M3 10.5 12 3l9 7.5"></path><path d="M5 9.5V21h14V9.5"></path>'
             '<path d="M10 21v-6h4v6"></path></svg>')

BAR_CSS = """<style>
.ps-bar{position:sticky;top:0;z-index:50;display:flex;align-items:center;flex-wrap:wrap;gap:6px 10px;
  padding:8px clamp(16px,3vw,40px);background:rgba(255,255,255,.94);backdrop-filter:blur(6px);
  border-bottom:1px solid #D5DEE3;font-family:'IBM Plex Sans Thai',system-ui,sans-serif;font-size:15px;color:#4A5D6A}
.ps-bar a{display:inline-flex;align-items:center;gap:6px;min-height:44px;padding:0 12px;border-radius:999px;
  color:#0A6A94;font-weight:600;text-decoration:none}
.ps-bar a:hover{background:#EAF3F7}
.ps-bar a:focus-visible{outline:3px solid #B04A0C;outline-offset:2px}
.ps-bar .ps-home{background:#0F2A3A;color:#FFFFFF}
.ps-bar .ps-home:hover{background:#163A4F}
.ps-bar [aria-current]{font-weight:600;color:#0F2A3A}
</style>"""


def crumb_bar(crumbs):
    """crumbs: list of (label, href); href '' marks the current page."""
    if not crumbs:
        return ""
    parts = []
    for i, (label, href) in enumerate(crumbs):
        if i:
            parts.append('<span aria-hidden="true">›</span>')
        if i == 0:
            parts.append(f'<a class="ps-home" href="{href}">{HOME_ICON}{label}</a>')
        elif href:
            parts.append(f'<a href="{href}">{label}</a>')
        else:
            parts.append(f'<span aria-current="page">{label}</span>')
    return '<nav class="ps-bar" aria-label="เส้นทางนำทาง">' + "".join(parts) + "</nav>\n"


def convert(src: str, renames: dict, runtime: str, crumbs=None) -> str:
    head_m = re.search(r"<head>(.*?)</head>", src, re.S)
    head = head_m.group(1) if head_m else ""
    head = re.sub(r'<script src="\./support\.js"></script>',
                  f'<meta name="viewport" content="width=device-width, initial-scale=1">\n'
                  f'<script src="{runtime}" defer></script>', head)

    xdc = re.search(r"<x-dc>(.*?)</x-dc>", src, re.S).group(1)
    helmet_m = re.search(r"<helmet>(.*?)</helmet>", xdc, re.S)
    helmet = helmet_m.group(1).strip() if helmet_m else ""
    body = re.sub(r"<helmet>.*?</helmet>", "", xdc, flags=re.S).strip()

    script = re.search(r"(<script type=\"text/x-dc\" data-dc-script.*?</script>)", src, re.S).group(1)

    for old, new in renames.items():
        body = body.replace(f'href="{old}"', f'href="{new}"')

    lang_m = re.search(r'<html lang="([^"]+)"', src)
    lang = lang_m.group(1) if lang_m else "en"

    bar = crumb_bar(crumbs)
    return (
        f'<!doctype html>\n<html lang="{lang}">\n<head>{head.rstrip()}\n{helmet}\n{BAR_CSS if bar else ""}\n</head>\n<body>\n'
        f'{bar}<div id="dc-root"></div>\n<template id="dc-template">\n{body}\n</template>\n'
        f'{script}\n</body>\n</html>\n'
    )


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 1
    src_path, out_path = argv[1], argv[2]
    renames, runtime, crumbs = {}, "../shared/dc-runtime.js", []
    i = 3
    while i < len(argv):
        if argv[i] == "--crumb":
            label, href = argv[i + 1].split("=", 1)
            crumbs.append((label, href))
            i += 2
        elif argv[i] == "--rename":
            old, new = argv[i + 1].split("=", 1)
            renames[old] = new
            i += 2
        elif argv[i] == "--runtime":
            runtime = argv[i + 1]
            i += 2
        else:
            i += 1
    with open(src_path, encoding="utf-8") as f:
        src = f.read()
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(convert(src, renames, runtime, crumbs))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
