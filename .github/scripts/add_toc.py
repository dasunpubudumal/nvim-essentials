"""Insert a table of contents into an nbconvert-generated HTML page.

The contents list is built from the page's h2/h3 headings (the ones nbconvert
gives an id), starting at the first h2, and is placed just before that h2, so
it sits below the notebook's title banner.

Usage: python add_toc.py page.html
"""

import re
import sys

HEADING = re.compile(r'<h([23]) id="([^"]+)">(.*?)</h\1>', re.S)
ANCHOR = re.compile(r'<a class="anchor-link"[^>]*>.*?</a>', re.S)
TAG = re.compile(r"<[^>]+>")


def build_toc(headings):
    lines = ['<nav class="toc"><p><strong>📑 Contents</strong></p><ul>']
    in_sublist = False
    for level, anchor, title in headings:
        link = f'<a href="#{anchor}">{title}</a>'
        if level == "2":
            if in_sublist:
                lines.append("</ul>")
                in_sublist = False
            if len(lines) > 1:
                lines.append("</li>")
            lines.append(f"<li>{link}")
        else:
            if not in_sublist:
                lines.append("<ul>")
                in_sublist = True
            lines.append(f"<li>{link}</li>")
    if in_sublist:
        lines.append("</ul>")
    lines.append("</li></ul></nav><hr>")
    return "\n".join(lines)


def insert_toc(html):
    matches = list(HEADING.finditer(html))
    first = next((m for m in matches if m.group(1) == "2"), None)
    if first is None:
        return html

    headings = [
        (m.group(1), m.group(2), TAG.sub("", ANCHOR.sub("", m.group(3))).strip())
        for m in matches
        if m.start() >= first.start()
    ]
    first = first.start()
    return html[:first] + build_toc(headings) + "\n" + html[first:]


def main(path):
    with open(path, encoding="utf-8") as f:
        html = f.read()
    with open(path, "w", encoding="utf-8") as f:
        f.write(insert_toc(html))


if __name__ == "__main__":
    main(sys.argv[1])
