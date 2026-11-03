"""Build the sessions page (the site's index.html) from the day-NN notebooks.

Each day-NN/ folder with a notebook becomes a card. The card's title comes from
the notebook's "Day N: ..." heading, its topics from the ## headings, and a
heading starting with "TODO" marks the session as still in progress.

The day's own notebook is the one named day-*.ipynb. Any other notebook in the
folder (e.g. a session summary) is an extra page, published next to it as
day-NN/<slug>.html, where the slug is the file name in lowercase with dashes.

Usage: python build_index.py <template.html> <output.html>
       python build_index.py --pages   (lists the notebooks to convert)
"""

import glob
import html
import json
import os
import re
import sys

MD_HEADING = re.compile(r"^(#{1,3})\s+(.+?)\s*#*$", re.M)
HTML_HEADING = re.compile(r"<h([1-3])[^>]*>(.*?)</h\1>", re.S | re.I)
DAY_TITLE = re.compile(r"Day\s*0*(\d+)\s*[:\-–—]\s*(.+)", re.I)
TAG = re.compile(r"<[^>]+>")
WORDS_PER_MINUTE = 200
MAX_TOPICS = 6


def headings(markdown):
    """Yield (level, text) for markdown and inline-HTML headings, in order."""
    found = [(m.start(), len(m.group(1)), m.group(2)) for m in MD_HEADING.finditer(markdown)]
    found += [
        (m.start(), int(m.group(1)), html.unescape(TAG.sub("", m.group(2))))
        for m in HTML_HEADING.finditer(markdown)
    ]
    for _, level, text in sorted(found):
        yield level, text.strip()


def read_markdown(notebook):
    with open(notebook, encoding="utf-8") as f:
        cells = json.load(f)["cells"]
    return "\n\n".join(
        "".join(c["source"]) for c in cells if c["cell_type"] == "markdown"
    )


def minutes(markdown):
    words = len(TAG.sub(" ", markdown).split())
    return max(1, round(words / WORDS_PER_MINUTE))


def slug(notebook):
    name = os.path.splitext(os.path.basename(notebook))[0]
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def read_session(day_dir):
    notebooks = sorted(glob.glob(os.path.join(day_dir, "*.ipynb")))
    notebook = ([n for n in notebooks if os.path.basename(n).startswith("day-")] or notebooks)[0]
    markdown = read_markdown(notebook)

    title, topics, wip = None, [], False
    for level, text in headings(markdown):
        if text.upper().startswith("TODO"):
            wip = True
            continue
        match = DAY_TITLE.search(text)
        if title is None and match:
            title = match.group(2).strip()
        elif level == 2:
            topics.append(text)

    number = int(re.search(r"\d+", os.path.basename(day_dir)).group())
    extras = [
        {
            "file": os.path.basename(n),
            "slug": slug(n),
            "title": os.path.splitext(os.path.basename(n))[0],
            "minutes": minutes(read_markdown(n)),
        }
        for n in notebooks
        if n != notebook
    ]
    return {
        "dir": os.path.basename(day_dir),
        "file": os.path.basename(notebook),
        "number": number,
        "title": title or f"Day {number}",
        "topics": topics,
        "minutes": minutes(markdown),
        "wip": wip,
        "extras": extras,
    }


def card(s):
    shown = s["topics"][:MAX_TOPICS]
    if len(s["topics"]) > MAX_TOPICS:
        shown.append(f"…and {len(s['topics']) - MAX_TOPICS} more")
    topics = "\n".join(f"                <li>{html.escape(t)}</li>" for t in shown)
    mode = '<span class="mode wip">WIP</span>' if s["wip"] else '<span class="mode">READY</span>'
    return f"""        <li>
          <a class="card" href="{s['dir']}/">
            <div class="winbar"><span class="dots"><i></i><i></i><i></i></span>{s['dir']}/{html.escape(s['file'])}</div>
            <div class="buffer">
              <p class="day-num">Day {s['number']:02d}</p>
              <h3>{html.escape(s['title'])}</h3>
              <ul class="topics">
{topics}
              </ul>
            </div>
            <div class="statusline">{mode}<span class="spacer"></span><span>~{s['minutes']} min read</span><span>ipynb</span></div>
          </a>
        </li>"""


def find_sessions():
    """Every day-NN/ folder (in the current directory) that has a notebook."""
    days = sorted(
        d for d in glob.glob("day-*")
        if os.path.isdir(d) and glob.glob(os.path.join(d, "*.ipynb"))
    )
    return [read_session(d) for d in days]


def list_pages():
    """Print "notebook<TAB>day-dir<TAB>output-name" for every page to convert."""
    for s in find_sessions():
        print(f"{s['dir']}/{s['file']}\t{s['dir']}\tindex")
        for e in s["extras"]:
            print(f"{s['dir']}/{e['file']}\t{s['dir']}\t{e['slug']}")


def main(template_path, output_path):
    sessions = find_sessions()

    with open(template_path, encoding="utf-8") as f:
        page = f.read()
    page = page.replace("{{SESSIONS}}", "\n".join(card(s) for s in sessions))
    page = page.replace("{{COUNT}}", str(len(sessions)))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(page)


if __name__ == "__main__":
    if sys.argv[1:] == ["--pages"]:
        list_pages()
    else:
        main(sys.argv[1], sys.argv[2])
