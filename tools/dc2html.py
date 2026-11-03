#!/usr/bin/env python3
"""Convert a Design-canvas artboard (.dc.html) into a standalone page for this repo.

Usage:
    python3 tools/dc2html.py SRC.dc.html OUT.html [--rename Old.dc.html=new.html ...]

What it does:
  * moves the <helmet> block (fonts, page styles) into <head>
  * wraps the <x-dc> markup in <template id="dc-template"> and adds <div id="dc-root">
  * swaps the canvas's support.js for ../shared/dc-runtime.js
  * rewrites links between artboards using the --rename map
"""
import re
import sys


def convert(src: str, renames: dict, runtime: str) -> str:
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

    return (
        f'<!doctype html>\n<html lang="{lang}">\n<head>{head.rstrip()}\n{helmet}\n</head>\n<body>\n'
        f'<div id="dc-root"></div>\n<template id="dc-template">\n{body}\n</template>\n'
        f'{script}\n</body>\n</html>\n'
    )


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 1
    src_path, out_path = argv[1], argv[2]
    renames, runtime = {}, "../shared/dc-runtime.js"
    i = 3
    while i < len(argv):
        if argv[i] == "--rename":
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
        f.write(convert(src, renames, runtime))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
