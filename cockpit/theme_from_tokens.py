#!/usr/bin/env python3
"""Turn the Kairos design tokens into a relay-kit Cockpit theme file.

    python3 theme_from_tokens.py --tokens RECORDS/kairos/design/tokens-v0.1-proposed.json \
        --mark amber|blue --out THEME.json

The tokens are read from the private records at build time; nothing from them is committed here.
--mark picks the colour that carries the Kairos name (the open design question): amber is
identity.kairos, blue is identity.heraldic. Colours the tokens don't name (insets, hovers, tints)
are mixed from the ones they do, so every surface follows the tokens. Standard library only.
"""
import argparse
import json
import pathlib
import sys


def hx(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def mix(a, b, t):
    """a moved toward b by t (0..1), as #rrggbb."""
    x, y = hx(a), hx(b)
    return "#" + "".join(f"{round(p + (q - p) * t):02x}" for p, q in zip(x, y))


def val(tokens, mode, path):
    node = tokens[mode]
    for k in path.split("."):
        node = node[k]
    return node["value"]


def palette(tokens, mode, mark):
    v = lambda p: val(tokens, mode, p)
    bg, panel, text, muted = v("surface.bg"), v("surface.panel"), v("surface.text"), v("surface.muted")
    border, line = v("surface.border"), v("surface.line")
    dark = mode == "dark"
    ink = "#000000" if dark else "#ffffff"
    ok, needs, blocked, stale = v("status.ok"), v("status.needs_owner"), v("status.blocked"), v("status.stale")
    verd, kit, tool, content = v("identity.verdigris"), v("identity.family.kit"), v("identity.family.tool"), v("identity.family.content")
    name_colour = v("identity.kairos") if mark == "amber" else v("identity.heraldic")
    return {
        "bg": bg, "sunk": mix(bg, ink, .18 if dark else .03), "panel": panel, "panel-2": mix(panel, text, .035),
        "field": mix(panel, text, .05), "field-hover": mix(panel, text, .10),
        "border": mix(panel, line, .45), "border-strong": border, "border-hover": mix(border, text, .25),
        "line": mix(panel, line, .30),
        "text": text, "text-2": mix(text, muted, .55), "muted": muted, "soft": mix(muted, panel, .12 if dark else .05),
        # teal is the Cockpit's working accent (links, accept, active): the kit family / verdigris
        "teal": kit if dark else verd, "teal-hi": mix(kit if dark else verd, text, .35), "on-teal": bg if dark else "#ffffff",
        "teal-bg": mix(panel, verd, .16), "teal-deep": mix(panel, verd, .45),
        # gold marks what needs the owner: the needs_owner status colour
        "gold": needs, "gold-deep": mix(panel, needs, .45), "gold-bg": mix(panel, needs, .12),
        "purple": content, "purple-deep": mix(panel, content, .45), "purple-bg": mix(panel, content, .14),
        "coral": blocked, "blue": tool, "blue-bg": mix(panel, tool, .14), "ok": ok,
        "mark": name_colour, "mark-word": name_colour, "focus": v("surface.focus"),
        "display": '"Source Sans 3", ui-sans-serif, system-ui, "Segoe UI", Arial, sans-serif',
        "heading": 'Fraunces, Georgia, "Times New Roman", serif',
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--tokens", required=True, type=pathlib.Path)
    ap.add_argument("--mark", choices=["amber", "blue"], default="amber")
    ap.add_argument("--default", choices=["auto", "dark", "light"], default="auto")
    ap.add_argument("--out", required=True, type=pathlib.Path)
    a = ap.parse_args(argv)
    try:
        tokens = json.loads(a.tokens.read_text(encoding="utf-8"))
        theme = {"name": f"kairos-{a.mark}-mark", "default": a.default,
                 "dark": palette(tokens, "dark", a.mark), "light": palette(tokens, "light", a.mark)}
    except (OSError, ValueError, KeyError) as x:
        sys.exit(f"refused: {a.tokens}: {x!r}")
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(theme, indent=1) + "\n", encoding="utf-8")
    print(f"theme written to {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
