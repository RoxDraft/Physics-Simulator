#!/usr/bin/env python3
"""Convert a Design-canvas artboard (.dc.html) into a standalone page for this repo.

Usage:
    python3 tools/dc2html.py SRC.dc.html OUT.html [options]

Options:
  --rename Old.dc.html=new.html   rewrite links between artboards
  --runtime PATH                  path to dc-runtime.js (default ../shared/dc-runtime.js)
  --crumb "Label=href"            adds a sticky top bar; the first crumb is the home
                                  button, an empty href marks the current page
  --alt "Label=href"              language switch button at the right of the top bar
  --lang en --dict FILE.json      translate every Thai text segment with the dictionary
                                  (keys "text@File.dc.html" override per file); the build
                                  fails if any Thai text is left untranslated
  --plain                         SRC is an ordinary HTML page: only translate it,
                                  apply --replace pairs and set <html lang>
  --replace "old=>new"            literal text replacement (with --plain)

tools/build.sh holds the exact commands for this repo.
"""
import json
import os
import re
import sys

THAI_SEGMENT = re.compile(r'[^<>"\'{}\n`]*[฀-๿][^<>"\'{}\n`]*')

HOME_ICON = ('<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
             'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
             '<path d="M3 10.5 12 3l9 7.5"></path><path d="M5 9.5V21h14V9.5"></path>'
             '<path d="M10 21v-6h4v6"></path></svg>')

GLOBE_ICON = ('<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
              'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
              '<circle cx="12" cy="12" r="9"></circle><path d="M3 12h18"></path>'
              '<path d="M12 3a14 14 0 0 1 0 18a14 14 0 0 1 0-18"></path></svg>')

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
.ps-bar .ps-lang{margin-left:auto;border:1.5px solid #0A6A94}
</style>"""

LANG_SCRIPT = ('<script>document.addEventListener("click",function(e){var a=e.target.closest&&'
               'e.target.closest("a[data-ps-lang]");if(a){try{localStorage.setItem("ps-lang",'
               'a.getAttribute("data-ps-lang"))}catch(_){}}});</script>')


# ---------- translation ----------
def translate(src: str, table: dict, filename: str) -> str:
    missing = []

    def sub(m):
        seg = m.group(0)
        core = seg.strip()
        if not core:
            return seg
        lead = seg[: len(seg) - len(seg.lstrip())]
        trail = seg[len(seg.rstrip()):]
        out = table.get(core + "@" + filename, table.get(core))
        if out is None:
            missing.append(core)
            return seg
        return lead + out + trail

    result = THAI_SEGMENT.sub(sub, src)
    if missing:
        raise SystemExit(f"{filename}: {len(missing)} untranslated segment(s):\n  " + "\n  ".join(missing[:20]))
    return result


# ---------- top bar ----------
def crumb_bar(crumbs, alt=None, lang="th"):
    """crumbs: list of (label, href); href '' marks the current page."""
    if not crumbs and not alt:
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
    if alt:
        label, href = alt
        target = "th" if lang == "en" else "en"
        switch = "เปลี่ยนเป็นภาษาอังกฤษ" if target == "en" else "Switch to Thai"
        parts.append(f'<a class="ps-lang" href="{href}" hreflang="{target}" lang="{target}" '
                     f'data-ps-lang="{target}" aria-label="{switch}">{GLOBE_ICON}{label}</a>')
    nav_label = "Breadcrumb" if lang == "en" else "เส้นทางนำทาง"
    return f'<nav class="ps-bar" aria-label="{nav_label}">' + "".join(parts) + "</nav>\n"


def convert(src: str, renames: dict, runtime: str, crumbs=None, alt=None) -> str:
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

    bar = crumb_bar(crumbs or [], alt, lang)
    extra = (BAR_CSS + "\n" + (LANG_SCRIPT if alt else "")) if bar else ""
    return (
        f'<!doctype html>\n<html lang="{lang}">\n<head>{head.rstrip()}\n{helmet}\n{extra}\n</head>\n<body>\n'
        f'{bar}<div id="dc-root"></div>\n<template id="dc-template">\n{body}\n</template>\n'
        f'{script}\n</body>\n</html>\n'
    )


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 1
    src_path, out_path = argv[1], argv[2]
    renames, runtime, crumbs, alt = {}, "../shared/dc-runtime.js", [], None
    lang, dict_path, plain, replaces = None, None, False, []
    i = 3
    while i < len(argv):
        a = argv[i]
        if a == "--crumb":
            label, href = argv[i + 1].split("=", 1)
            crumbs.append((label, href))
        elif a == "--alt":
            label, href = argv[i + 1].split("=", 1)
            alt = (label, href)
        elif a == "--rename":
            old, new = argv[i + 1].split("=", 1)
            renames[old] = new
        elif a == "--runtime":
            runtime = argv[i + 1]
        elif a == "--lang":
            lang = argv[i + 1]
        elif a == "--dict":
            dict_path = argv[i + 1]
        elif a == "--replace":
            old, new = argv[i + 1].split("=>", 1)
            replaces.append((old, new))
        elif a == "--plain":
            plain = True
            i += 1
            continue
        else:
            i += 1
            continue
        i += 2

    with open(src_path, encoding="utf-8") as f:
        src = f.read()
    if dict_path:
        with open(dict_path, encoding="utf-8") as f:
            table = json.load(f)
        src = translate(src, table, os.path.basename(src_path))
    if lang:
        src = re.sub(r'<html lang="[^"]*"', f'<html lang="{lang}"', src, count=1)

    if plain:
        out = src
        for old, new in replaces:
            if old not in out:
                raise SystemExit(f"--replace: {old!r} not found in {src_path}")
            out = out.replace(old, new)
    else:
        out = convert(src, renames, runtime, crumbs, alt)

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
