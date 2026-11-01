"""Dress each nbconvert page in the Neovim Essentials theme.

For every session's <site>/day-NN/index.html this sets a proper title, links
the favicons, fonts, theme.css and notebook.css, inserts the table of contents,
and wraps the notebook in Neovim-style chrome: a tabline of all sessions, a
reading-progress bar, previous/next links, and a sticky statusline. j/k scroll,
gg/G jump to the top/bottom, and H/L go to the previous/next session (as in
LazyVim).

Usage: python style_notebooks.py <site_dir>   (run from the repository root)
"""

import html
import os
import re
import sys

from add_toc import insert_toc
from build_index import find_sessions

HEAD = """<link rel="icon" href="../favicon.ico" sizes="32x32">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="../apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../theme.css">
<link rel="stylesheet" href="../notebook.css">
"""

SCRIPT = """<script>
  (function () {
    var root = document.documentElement;
    var pos = document.querySelector(".bottombar .pos");
    function update() {
      var max = root.scrollHeight - root.clientHeight;
      var y = root.scrollTop;
      var ratio = max > 0 ? Math.min(y / max, 1) : 1;
      root.style.setProperty("--read", ratio);
      pos.textContent = y <= 0 ? "Top" : ratio >= 1 ? "Bot" : Math.round(ratio * 100) + "%";
    }
    addEventListener("scroll", update, { passive: true });
    addEventListener("resize", update);
    update();

    // Vim-style keys. "g" must be pressed twice (gg), like in Neovim.
    var lastG = 0;
    document.addEventListener("keydown", function (e) {
      if (e.ctrlKey || e.metaKey || e.altKey || /input|textarea|select/i.test(e.target.tagName)) return;
      var step = 80, link;
      if (e.key === "j") scrollBy({ top: step });
      else if (e.key === "k") scrollBy({ top: -step });
      else if (e.key === "G") scrollTo({ top: root.scrollHeight });
      else if (e.key === "g") {
        if (Date.now() - lastG < 500) scrollTo({ top: 0 });
        lastG = Date.now();
      }
      else if (e.key === "H" && (link = document.querySelector(".pager .prev"))) location.href = link.href;
      else if (e.key === "L" && (link = document.querySelector(".pager .next"))) location.href = link.href;
      else return;
      e.preventDefault();
    });
  })();
</script>
"""


def tabline(sessions, current):
    tabs = ['<nav class="tabline" aria-label="Sessions">', '<a href="../">sessions.md</a>']
    for s in sessions:
        if s is current:
            tabs.append(f'<span class="active" aria-current="page">{s["dir"]}</span>')
        else:
            tabs.append(f'<a href="../{s["dir"]}/">{s["dir"]}</a>')
    tabs.append('<span class="fill"></span><span>nvim-essentials</span></nav>')
    return "".join(tabs)


def pager(prev, nxt):
    links = []
    if prev:
        links.append(
            f'<a class="prev" href="../{prev["dir"]}/"><small>← Day {prev["number"]:02d} · H</small>'
            f'<strong>{html.escape(prev["title"])}</strong></a>'
        )
    if nxt:
        links.append(
            f'<a class="next" href="../{nxt["dir"]}/"><small>Day {nxt["number"]:02d} · L →</small>'
            f'<strong>{html.escape(nxt["title"])}</strong></a>'
        )
    else:
        links.append('<a class="next" href="../"><small>All sessions →</small><strong>Back to the list</strong></a>')
    return f'<nav class="pager" aria-label="More sessions">{"".join(links)}</nav>'


def statusline(s):
    mode = '<span class="mode wip">WIP</span>' if s["wip"] else '<span class="mode">NORMAL</span>'
    return (
        f'<footer class="bottombar sticky">{mode}'
        f'<span>{s["dir"]}/{html.escape(s["file"])}</span>'
        f'<span class="optional">~{s["minutes"]} min read</span>'
        '<span class="spacer"></span>'
        '<a href="../" class="optional">:sessions</a>'
        '<span class="optional">utf-8</span>'
        '<span class="pos">Top</span></footer>'
    )


def style(page, sessions, i):
    s = sessions[i]
    prev = sessions[i - 1] if i > 0 else None
    nxt = sessions[i + 1] if i + 1 < len(sessions) else None

    title = f"Day {s['number']:02d} · {s['title']} | Neovim Essentials"
    page = re.sub(r"<title>.*?</title>", lambda _: f"<title>{html.escape(title)}</title>", page, count=1, flags=re.S)
    page = page.replace("</head>", HEAD + "</head>", 1)
    page = page.replace(
        "<main>",
        '<div class="progress" aria-hidden="true"></div>' + tabline(sessions, s) + '<main class="nb-buffer">',
        1,
    )
    page = page.replace("</main>", pager(prev, nxt) + "</main>" + statusline(s) + SCRIPT, 1)
    return insert_toc(page)


def main(site_dir):
    sessions = find_sessions()
    for i, s in enumerate(sessions):
        path = os.path.join(site_dir, s["dir"], "index.html")
        with open(path, encoding="utf-8") as f:
            page = f.read()
        with open(path, "w", encoding="utf-8") as f:
            f.write(style(page, sessions, i))


if __name__ == "__main__":
    main(sys.argv[1])
