"""Render index.html and problems/<slug>.html from problems.py.

Usage: python3 build.py
"""
from pathlib import Path

from problems import CATEGORIES, PROBLEMS

ROOT = Path(__file__).parent
UPDATED = "September 2026"

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{prefix}style.css">
</head>
<body>
<div class="wrap">
"""

FOOT = """  <footer>{note}Last updated {updated}.</footer>
</div>
</body>
</html>
"""

PICK = ' <span class="pick">easy to explain</span>'


def strip_tags(html):
    import re
    return re.sub(r"<[^>]+>", "", html).replace('"', "&quot;")


def render_index():
    out = [HEAD.format(
        title="Open Problems in Mathematics",
        description="Important open problems in mathematics that are easy to explain, from number theory to graph theory.",
        prefix="",
    )]
    out.append("""  <header>
    <h1>Open Problems in Mathematics</h1>
    <p>Famous unsolved problems that are easy to state. Click any problem for its history, current status, why it matters, and ideas for attacking it. Problems tagged <span class="pick">easy to explain</span> are especially good for a general audience: you can try examples by hand.</p>
    <nav class="toc">
""")
    for cid, name, _ in CATEGORIES:
        out.append(f'      <a href="#{cid}">{name}</a>\n')
    out.append("    </nav>\n  </header>\n")

    n = 0
    for cid, name, intro in CATEGORIES:
        out.append(f'\n  <section id="{cid}">\n    <h2>{name}</h2>\n')
        if intro:
            out.append(f'    <p class="intro">{intro}</p>\n')
        out.append('    <ol class="cards">\n')
        for p in PROBLEMS:
            if p["cat"] != cid:
                continue
            n += 1
            href = f'problems/{p["slug"]}.html'
            out.append(f'      <li><span class="n">{n}</span>\n')
            out.append(f'        <h3><a href="{href}">{p["title"]}</a>{PICK if p["pick"] else ""}</h3>\n')
            out.append(f'        <p>{p["short"]}</p>\n')
            if p["short_status"]:
                out.append(f'        <p class="status">{p["short_status"]}</p>\n')
            out.append(f'        <a class="more" href="{href}">History, status and approaches →</a>\n')
            out.append("      </li>\n")
        out.append("    </ol>\n  </section>\n")

    out.append(FOOT.format(note="", updated=UPDATED))
    (ROOT / "index.html").write_text("".join(out))


def paragraphs(items, indent="      "):
    return "".join(
        f"{indent}{t}\n" if t.lstrip().startswith("<ul>") else f"{indent}<p>{t}</p>\n"
        for t in items
    )


def render_problem(i, p):
    cat_name = next(name for cid, name, _ in CATEGORIES if cid == p["cat"])
    out = [HEAD.format(
        title=f'{p["title"]} · Open Problems',
        description=strip_tags(p["short"]),
        prefix="../",
    )]
    out.append(f"""  <div class="crumbs"><a href="../index.html">← All open problems</a></div>
  <article>
    <header>
      <div class="kicker">Problem {i + 1} · {cat_name}</div>
      <h1>{p["title"]}</h1>
      <p>{p["short"]}</p>
    </header>
    <div class="statement"><strong>Statement.</strong> {p["statement"]}</div>
    <div class="facts">
""")
    for k, v in p["facts"]:
        out.append(f'      <div class="fact"><div class="k">{k}</div><div class="v">{v}</div></div>\n')
    out.append("    </div>\n")

    out.append('\n    <section>\n      <h2>Why it matters</h2>\n')
    out.append(paragraphs(p["importance"]))
    out.append('    </section>\n\n    <section>\n      <h2>Where things stand</h2>\n')
    out.append(paragraphs(p["status"]))
    out.append('    </section>\n\n    <section>\n      <h2>History of attempts</h2>\n      <ul class="timeline">\n')
    for yr, text in p["timeline"]:
        out.append(f'        <li><span class="yr">{yr}</span>{text}</li>\n')
    out.append('      </ul>\n    </section>\n\n    <section>\n      <h2>Ideas for solving it</h2>\n      <ul>\n')
    for a in p["approaches"]:
        out.append(f"        <li>{a}</li>\n")
    out.append("      </ul>\n    </section>\n")
    if p["try_it"]:
        out.append(f'\n    <section class="try">\n      <h2>Try it yourself</h2>\n      <p>{p["try_it"]}</p>\n    </section>\n')
    out.append("  </article>\n\n  <nav class=\"pager\">\n")
    if i > 0:
        prev = PROBLEMS[i - 1]
        out.append(f'    <a class="prev" href="{prev["slug"]}.html">← {prev["title"]}</a>\n')
    if i < len(PROBLEMS) - 1:
        nxt = PROBLEMS[i + 1]
        out.append(f'    <a class="next" href="{nxt["slug"]}.html">{nxt["title"]} →</a>\n')
    out.append("  </nav>\n")
    out.append(FOOT.format(
        note="Status reflects published results as of the date below; recent claims may still be under review. ",
        updated=UPDATED,
    ))
    return "".join(out)


def main():
    render_index()
    outdir = ROOT / "problems"
    outdir.mkdir(exist_ok=True)
    for i, p in enumerate(PROBLEMS):
        (outdir / f'{p["slug"]}.html').write_text(render_problem(i, p))
    print(f"Wrote index.html and {len(PROBLEMS)} problem pages.")


if __name__ == "__main__":
    main()
