#!/usr/bin/env python3
"""Render the two papers in docs/papers/ from Markdown to HTML using site.css.

Standard library only. Handles headings, paragraphs, bullet and numbered
lists (one level of nesting by indentation), fenced and indented code,
block quotes, simple pipe tables, bold, italic, inline code and links.
Anything else is passed through as paragraph text.

Usage:  python3 docs/tools/render_papers.py
"""
from __future__ import annotations

import html
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
DOCS = HERE.parent
PAPERS = DOCS / "papers"

SOURCES = [
    ("01-reason-attached-to-the-work", "The reason attached to the work"),
    ("02-measuring-whether-coordination-helps", "Measuring whether coordination helps"),
]

LABEL = (
    "Preliminary draft, agent-drafted from the project records; "
    "the owner has not yet reviewed or endorsed this text."
)

NAV = [
    ("index.html", "Overview"),
    ("tools.html", "Tools"),
    ("start.html", "Contribute"),
    ("how-we-work.html", "How we work"),
    ("papers.html", "Papers"),
]


# ---------------------------------------------------------------- inline

_INLINE = [
    (re.compile(r"`([^`]+)`"), lambda m: f"<code>{html.escape(m.group(1))}</code>"),
    (re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)"), lambda m: f'<a href="{html.escape(m.group(2), quote=True)}">{m.group(1)}</a>'),
    (re.compile(r"\*\*(.+?)\*\*"), lambda m: f"<strong>{m.group(1)}</strong>"),
    (re.compile(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])"), lambda m: f"<em>{m.group(1)}</em>"),
    (re.compile(r"(?<![\w_])_(?!\s)(.+?)(?<!\s)_(?![\w_])"), lambda m: f"<em>{m.group(1)}</em>"),
]


def inline(text: str) -> str:
    """Escape, then apply inline markup. Code spans are protected first."""
    parts = re.split(r"(`[^`]+`)", text)
    out = []
    for part in parts:
        if part.startswith("`") and part.endswith("`") and len(part) > 1:
            out.append(f"<code>{html.escape(part[1:-1])}</code>")
            continue
        s = html.escape(part, quote=False)
        for rx, fn in _INLINE[1:]:
            s = rx.sub(fn, s)
        out.append(s)
    return "".join(out)


# ---------------------------------------------------------------- blocks

def render_markdown(md: str) -> tuple[str, str | None]:
    """Return (html_body, first_h1_text)."""
    lines = md.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    title: str | None = None
    i = 0
    n = len(lines)

    def flush_para(buf: list[str]) -> None:
        if buf:
            out.append(f"<p>{inline(' '.join(s.strip() for s in buf))}</p>")
            buf.clear()

    para: list[str] = []

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # blank
        if not stripped:
            flush_para(para)
            i += 1
            continue

        # fenced code
        if stripped.startswith("```"):
            flush_para(para)
            i += 1
            code: list[str] = []
            while i < n and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1  # closing fence
            out.append(f"<pre><code>{html.escape(chr(10).join(code))}</code></pre>")
            continue

        # heading
        m = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", stripped)
        if m:
            flush_para(para)
            level = len(m.group(1))
            text = m.group(2)
            if level == 1 and title is None:
                title = re.sub(r"[*_`]", "", text)
            hid = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
            out.append(f'<h{level} id="{hid}">{inline(text)}</h{level}>')
            i += 1
            continue

        # horizontal rule
        if re.match(r"^(-{3,}|\*{3,}|_{3,})$", stripped):
            flush_para(para)
            out.append("<hr>")
            i += 1
            continue

        # block quote
        if stripped.startswith(">"):
            flush_para(para)
            quote: list[str] = []
            while i < n and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip()[1:].strip())
                i += 1
            inner, _ = render_markdown("\n".join(quote))
            out.append(f"<blockquote>{inner}</blockquote>")
            continue

        # table
        if "|" in stripped and i + 1 < n and re.match(r"^\s*\|?\s*:?-{2,}", lines[i + 1]):
            flush_para(para)
            rows: list[str] = []
            while i < n and "|" in lines[i].strip():
                rows.append(lines[i].strip())
                i += 1
            cells = lambda r: [c.strip() for c in r.strip("|").split("|")]
            head = cells(rows[0])
            body = [cells(r) for r in rows[2:]]
            t = ["<table><thead><tr>"]
            t += [f"<th>{inline(c)}</th>" for c in head]
            t.append("</tr></thead><tbody>")
            for r in body:
                t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table>")
            out.append("".join(t))
            continue

        # lists (bullet or numbered, with one level of nesting by indent)
        if re.match(r"^\s*([-*+]|\d+[.)])\s+", line):
            flush_para(para)
            block: list[str] = []
            while i < n and (re.match(r"^\s*([-*+]|\d+[.)])\s+", lines[i]) or (lines[i].startswith("  ") and lines[i].strip())):
                block.append(lines[i])
                i += 1
            out.append(render_list(block))
            continue

        # indented code (4 spaces) when not inside a list
        if line.startswith("    ") and not para:
            flush_para(para)
            code = []
            while i < n and (lines[i].startswith("    ") or not lines[i].strip()):
                code.append(lines[i][4:] if lines[i].startswith("    ") else "")
                i += 1
            while code and not code[-1]:
                code.pop()
            out.append(f"<pre><code>{html.escape(chr(10).join(code))}</code></pre>")
            continue

        para.append(line)
        i += 1

    flush_para(para)
    return "\n".join(out), title


def render_list(block: list[str]) -> str:
    """Render a list block. Nesting is by indentation (2+ spaces)."""
    items: list[tuple[int, str, list[str]]] = []  # (indent, marker, lines)
    for ln in block:
        m = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$", ln)
        if m:
            items.append((len(m.group(1)), m.group(2), [m.group(3)]))
        elif items:
            items[-1][2].append(ln.strip())
    if not items:
        return ""
    base = items[0][0]
    ordered = items[0][1][0].isdigit()
    tag = "ol" if ordered else "ul"
    out = [f"<{tag}>"]
    k = 0
    while k < len(items):
        indent, marker, text = items[k]
        if indent <= base:
            # gather nested
            j = k + 1
            nested: list[str] = []
            while j < len(items) and items[j][0] > base:
                ind, mk, tx = items[j]
                nested.append(" " * ind + mk + " " + " ".join(tx))
                j += 1
            body = inline(" ".join(text))
            if nested:
                body += render_list(nested)
            out.append(f"<li>{body}</li>")
            k = j
        else:
            k += 1
    out.append(f"</{tag}>")
    return "".join(out)


# ---------------------------------------------------------------- page

def page(title: str, body: str, slug: str) -> str:
    nav = "\n        ".join(
        f'<li><a href="../{href}"{" aria-current=\"page\"" if href == "papers.html" else ""}>{label}</a></li>'
        for href, label in NAV
    )
    return f"""<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}, Kairos</title>
<meta name="description" content="{html.escape(LABEL, quote=True)}">
<link rel="stylesheet" href="../site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="bar">
    <a class="wordmark" href="../index.html"><span class="mark" aria-hidden="true"></span><span class="name">Kairos</span></a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <button class="theme-toggle" type="button">Theme: auto</button>
    <nav class="site-nav" id="site-nav" aria-label="Site">
      <ul>
        {nav}
      </ul>
    </nav>
  </div>
</header>
<main id="main">
<p><a href="../papers.html">All papers</a></p>
<p><span class="draft-label">{html.escape(LABEL)}</span></p>
<article class="paper-body">
{body}
</article>
<p class="aside">Rendered from <a href="{slug}.md">{slug}.md</a> by <code>docs/tools/render_papers.py</code>.</p>
</main>
<footer class="site-footer">
  <div class="inner">
    <p><span class="name">Kairos</span> is Zach Rhodes's project. Site generated by a Claude agent on 2026-11-06 from the START HERE README; no analytics, no cookies, no external requests.</p>
    <p>Public repos are MIT. Each carries a <code>CLA.md</code>: contributing grants the owner a commercial-relicensing right so companies can use the code with minimal risk while he keeps his rights. Read it before your first PR.</p>
  </div>
</footer>
<script src="../site.js"></script>
</body>
</html>
"""


def main() -> int:
    rendered = 0
    for slug, fallback_title in SOURCES:
        src = PAPERS / f"{slug}.md"
        dst = PAPERS / f"{slug}.html"
        if not src.exists():
            print(f"note: {src.relative_to(DOCS.parent)} not present; {dst.name} not written")
            continue
        body, title = render_markdown(src.read_text(encoding="utf-8"))
        dst.write_text(page(title or fallback_title, body, slug), encoding="utf-8")
        print(f"wrote {dst.relative_to(DOCS.parent)}")
        rendered += 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
