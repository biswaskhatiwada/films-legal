# -*- coding: utf-8 -*-
"""
build.py — render The Journal into films-legal/blog/.

Authoring tooling only: the *output* under blog/ is plain static HTML/CSS/SVG
(no runtime build step on the deployed site). Run from anywhere:

    python3 journal-src/build.py

Reads posts.py (metadata) + content/<slug>.html (body) + covers.py (art),
writes blog/index.html, blog/<slug>.html, and blog/art/<slug>.svg.
"""

import os
from datetime import datetime

import covers
from posts import POSTS, CATS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG = os.path.join(ROOT, "blog")
ART = os.path.join(BLOG, "art")
CONTENT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "content")
BASE = "https://biswaskhatiwada.github.io/films-legal"

SPARK = ('<svg class="spark" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">'
         '<path d="M50 2 C53 30 70 47 98 50 C70 53 53 70 50 98 C47 70 30 53 2 50 '
         'C30 47 47 30 50 2 Z" fill="#E6B450"/></svg>')

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"/>'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>'
         '<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1'
         '&family=Hanken+Grotesk:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700'
         '&display=swap" rel="stylesheet"/>')


def pretty(iso):
    return datetime.strptime(iso, "%Y-%m-%d").strftime("%B %-d, %Y")


def nav(prefix=""):
    return f'''<nav><div class="wrap">
    <a class="logo" href="{prefix}../index.html">{SPARK}Films</a>
    <div class="navlinks">
      <a href="{prefix}../index.html#looks">Looks</a>
      <a href="{prefix}../index.html#reveal">Reveal</a>
      <a href="{prefix}index.html" class="active">Journal</a>
      <a class="btn" href="{prefix}../index.html#waitlist">Join the waitlist</a>
    </div></div></nav>'''


def footer(prefix=""):
    return f'''<footer><div class="wrap">
    <div class="logo">{SPARK}Films</div>
    <div class="links">
      <a href="index.html">Journal</a>
      <a href="{prefix}../privacy.html">Privacy</a>
      <a href="{prefix}../terms.html">Terms</a>
      <a href="{prefix}../support.html">Support</a>
    </div>
    <div>© 2026 Films</div>
  </div></footer>'''


def cta_band():
    return '''<section><div class="wrap"><div class="band reveal">
      <span class="pill">Be first</span>
      <h2>Be the first to shoot a roll.</h2>
      <p>Films is coming to the App Store. Leave your email and we'll send one message the day it lands.</p>
      <a class="btn" href="../index.html#waitlist">Join the waitlist</a>
    </div></div></section>'''


def card(p):
    return f'''<a class="card reveal" data-cat="{p['cat']}" href="{p['slug']}.html">
      <div class="art"><img loading="lazy" src="art/{p['slug']}.svg" alt="{p['title']} — cover illustration"/></div>
      <div class="body">
        <div class="meta"><span class="cat">{p['cat']}</span><span>·</span><span>{p['read']} min read</span></div>
        <h3>{p['title']}</h3>
        <p>{p['excerpt']}</p>
        <span class="more">Read the story →</span>
      </div></a>'''


def related_for(post):
    same = [q for q in POSTS if q["cat"] == post["cat"] and q["slug"] != post["slug"]]
    others = [q for q in POSTS if q["cat"] != post["cat"] and q["slug"] != post["slug"]]
    picks = (same + others)[:3]
    cards = "".join(card(p) for p in picks)
    return f'''<section class="related"><div class="wrap">
      <div class="lbl">Keep reading</div>
      <div class="grid">{cards}</div></div></section>'''


def head(title, desc, slug):
    return f'''<!DOCTYPE html><html lang="en"><head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"/>
<title>{title} — The Journal · Films</title>
<meta name="description" content="{desc}"/>
<meta name="theme-color" content="#0A0807"/>
<meta property="og:title" content="{title}"/>
<meta property="og:description" content="{desc}"/>
<meta property="og:type" content="article"/>
<meta property="og:image" content="{BASE}/blog/art/{slug}.svg"/>
<meta property="og:url" content="{BASE}/blog/{slug}.html"/>
<meta name="twitter:card" content="summary_large_image"/>
{FONTS}
<link rel="stylesheet" href="journal.css"/>
</head><body>'''


def build_cover(p):
    a, b = CATS[p["cat"]]
    svg = covers.cover_svg(p["slug"], p["motif"], a, b)
    with open(os.path.join(ART, f"{p['slug']}.svg"), "w") as f:
        f.write(svg)


def build_article(p):
    frag = os.path.join(CONTENT, f"{p['slug']}.html")
    if os.path.exists(frag):
        with open(frag) as f:
            body = f.read()
    else:
        body = "<p>Coming soon.</p>"
    divider = f'<div class="divider">{covers.divider_svg(CATS[p["cat"]][0])}</div>'
    body = body.replace("{{divider}}", divider)

    html = head(p["title"], p["excerpt"], p["slug"])
    html += nav()
    html += f'''<article>
  <div class="wrap"><header class="article-hero">
    <span class="pill">{p['cat']}</span>
    <h1>{p['title']}</h1>
    <p class="dek">{p['dek']}</p>
    <div class="byline"><span>Films</span><span class="dot">·</span>
      <time datetime="{p['date']}">{pretty(p['date'])}</time>
      <span class="dot">·</span><span>{p['read']} min read</span></div>
  </header></div>
  <div class="wrap"><figure class="cover">
    <img src="art/{p['slug']}.svg" alt="{p['title']} — cover illustration"/>
  </figure></div>
  <div class="wrap"><div class="prose">{body}</div></div>
  <div class="wrap"><div class="end-note">
    <div class="mark">{SPARK}</div>
    <div><h4>Written by the Films team</h4>
    <p>Films is a shared disposable camera — everyone shoots the same moment through vintage looks, and nobody sees a frame until it develops. <a href="../index.html#waitlist" style="color:var(--brass)">Join the waitlist →</a></p></div>
  </div></div>
</article>'''
    html += related_for(p)
    html += cta_band()
    html += footer()
    html += '<script src="journal.js"></script></body></html>'

    with open(os.path.join(BLOG, f"{p['slug']}.html"), "w") as f:
        f.write(html)


def build_index():
    feat = POSTS[0]
    rest = POSTS[1:]
    cats = list(CATS.keys())
    filters = '<button class="filter on" data-filter="all">All</button>' + "".join(
        f'<button class="filter" data-filter="{c}">{c}</button>' for c in cats)
    grid = "".join(card(p) for p in rest)

    html = f'''<!DOCTYPE html><html lang="en"><head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"/>
<title>The Journal — Films</title>
<meta name="description" content="Notes on film, memory, and shooting together — from the team behind Films, the shared disposable camera."/>
<meta name="theme-color" content="#0A0807"/>
<meta property="og:title" content="The Journal — Films"/>
<meta property="og:description" content="Notes on film, memory, and shooting together."/>
<meta property="og:type" content="website"/>
<meta property="og:image" content="{BASE}/blog/art/{feat['slug']}.svg"/>
<meta property="og:url" content="{BASE}/blog/"/>
{FONTS}
<link rel="stylesheet" href="journal.css"/>
</head><body>'''
    html += nav()
    html += '''<header class="j-head"><div class="wrap">
    <span class="pill">The Journal</span>
    <h1>Notes on film, memory, and shooting together.</h1>
    <p>Stories on the looks, the wait, and the craft of capturing a night the way it actually felt — from the team behind Films.</p>
  </div></header>'''
    html += f'''<div class="wrap"><article class="featured reveal">
    <div class="art"><a href="{feat['slug']}.html"><img loading="lazy" src="art/{feat['slug']}.svg" alt="{feat['title']} — cover illustration"/></a></div>
    <div class="copy">
      <div class="meta"><span class="pill">Featured</span><span>{feat['cat']}</span><span>·</span><span>{feat['read']} min read</span></div>
      <h2><a href="{feat['slug']}.html">{feat['title']}</a></h2>
      <p class="ex">{feat['excerpt']}</p>
      <a class="read" href="{feat['slug']}.html">Read the story →</a>
    </div></article></div>'''
    html += f'''<div class="wrap">
    <div class="filters">{filters}</div>
    <div class="grid">{grid}</div>
  </div>'''
    html += cta_band()
    html += footer()
    html += '<script src="journal.js"></script></body></html>'

    with open(os.path.join(BLOG, "index.html"), "w") as f:
        f.write(html)


def main():
    os.makedirs(ART, exist_ok=True)
    for p in POSTS:
        build_cover(p)
        build_article(p)
    build_index()
    have = sum(1 for p in POSTS if os.path.exists(os.path.join(CONTENT, f"{p['slug']}.html")))
    print(f"Built {len(POSTS)} covers + {len(POSTS)} articles + index. "
          f"Content fragments present: {have}/{len(POSTS)}.")


if __name__ == "__main__":
    main()
