"""Build three local, content-identical LinkedIn materials page alternatives."""

from html import escape
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOCIAL = HERE.parent
source = (SOCIAL / "linkedin-post.md").read_text()


def section(start: str, end: str | None = None) -> str:
    body = source.split(f"# {start}\n", 1)[1]
    if end:
        body = body.split(f"# {end}\n", 1)[0]
    return body.strip()


headline = section("Headline", "Post")
post = section("Post", "Image alt text")
alt = section("Image alt text")


def editor(name: str, value: str, rows: int, copy_label: str) -> str:
    return f"""<div class="editor-block">
      <div class="editor-heading"><label for="{name}">{escape(name.replace('-', ' ').title())}</label><span>{len(value.split())} words</span></div>
      <textarea id="{name}" name="{name}" rows="{rows}" spellcheck="true">{escape(value)}</textarea>
      <button type="button" class="copy-button" data-copy="{name}">{escape(copy_label)}</button>
    </div>"""


def downloads() -> str:
    return """<div class="download-row" aria-label="Graph downloads">
      <a class="download-link" href="../linkedin-graph.png" download="glp1-prior-authorization-graph.png">Download PNG <span>1600 × 2000</span></a>
      <a class="download-link" href="../linkedin-graph.svg" download="glp1-prior-authorization-graph.svg">Download editable SVG <span>vector</span></a>
    </div>"""


def figure() -> str:
    return """<figure class="graph-figure">
      <img src="../linkedin-graph.png" width="1600" height="2000" alt="Graph of the nine declared policy edges, followed by a citation gate and human review. The graphic labels the policy and test cases synthetic." fetchpriority="high">
      <figcaption>Actual nine-edge demo topology. The policy and test cases are synthetic; the published glp1-obesity CKG is not loaded in this demo.</figcaption>
    </figure>"""


def shell(title: str, body_class: str, content: str) -> str:
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="{('#092a2d' if body_class == 'control' else '#eef2ef' if body_class == 'editorial' else '#e9eef1')}">
<title>{escape(title)} · GLP-1 LinkedIn Materials</title><link rel="stylesheet" href="styles.css"></head>
<body class="{body_class}"><a class="skip-link" href="#main">Skip to materials</a>{content}
<div id="copy-status" class="sr-only" role="status" aria-live="polite"></div><script src="app.js" defer></script></body></html>"""


editorial = f"""<header class="ed-header"><a class="wordmark" href="comparison.html">Daniel Yarmoluk <span>/ GLP-1 materials</span></a><a class="back-link" href="comparison.html">Compare designs</a></header>
<main id="main" class="ed-main"><section class="ed-intro"><div><h1>A model can write.<br><em>It cannot invent an edge.</em></h1><p>A LinkedIn post, a traceable graph, and the words needed to publish them accurately.</p></div><div class="ed-index"><span>Materials</span><a href="#post">Post copy</a><a href="#graph">Graph image</a><a href="#alt">Image description</a></div></section>
<div class="ed-feature"><section id="post" class="ed-copy"><h2>Post copy</h2><p class="section-note">Edit the text here, then copy the version you want to publish.</p>{editor('headline', headline, 3, 'Copy headline')}{editor('post-text', post, 20, 'Copy full post')}</section><section id="graph" class="ed-visual"><div class="visual-heading"><h2>The graph</h2><p>Keep the diagram with the post.</p></div>{figure()}{downloads()}</section></div>
<section id="alt" class="ed-alt"><div><h2>Image description</h2><p>The complete alt text travels with the graphic when you upload it.</p></div>{editor('alt-text', alt, 8, 'Copy image alt text')}</section></main><footer class="ed-footer">Local comparison only · No LinkedIn publication</footer>"""

control = f"""<header class="ct-header"><a class="ct-brand" href="comparison.html">DY<span> / GLP-1</span></a><nav aria-label="Page"><a href="#graphic">Graphic</a><a href="#copy">Copy</a><a href="#description">Alt text</a><a href="comparison.html">All designs</a></nav></header>
<main id="main"><section class="ct-hero"><div class="ct-hero-copy"><h1>The model can write.<br><span>It cannot invent an edge.</span></h1><p>LinkedIn materials for the GLP-1 prior-authorization draft gate.</p><a class="ct-jump" href="#copy">Review the post <span aria-hidden="true">↘</span></a></div><div id="graphic" class="ct-art">{figure()}</div></section>
<section class="ct-downloads"><div><h2>Export the graph</h2><p>The full-resolution graphic and editable vector are ready for your post.</p></div>{downloads()}</section>
<section id="copy" class="ct-work"><div class="ct-work-title"><h2>Write once. Check every edge.</h2><p>The post below keeps the demo scope and test limits explicit.</p></div><div class="ct-editors">{editor('headline', headline, 3, 'Copy headline')}{editor('post-text', post, 20, 'Copy full post')}</div></section>
<section id="description" class="ct-alt"><div><h2>Image alt text</h2><p>Use this description when adding the image to LinkedIn.</p></div>{editor('alt-text', alt, 8, 'Copy image alt text')}</section></main><footer class="ct-footer">Local comparison only · No LinkedIn publication</footer>"""

studio = f"""<header class="st-header"><a class="st-logo" href="comparison.html">GLP-1 <span>Materials Studio</span></a><a href="comparison.html">Compare all three designs</a></header>
<main id="main" class="st-main"><div class="st-heading"><div><h1>Prepare the post</h1><p>Copy, inspect, and download from one workspace.</p></div><span class="st-state">Local draft</span></div>
<div class="st-grid"><aside class="st-rail" aria-label="Materials checklist"><h2>Materials</h2><a href="#copy">01 <span>Post & headline</span></a><a href="#preview">02 <span>Graph preview</span></a><a href="#accessibility">03 <span>Alt text</span></a><p>Demo scope: hand-written synthetic policy overlay and cases. No ckg-mcp or published glp1-obesity CKG is loaded.</p></aside>
<section id="preview" class="st-preview"><div class="st-panel-head"><h2>Graph preview</h2><span>1600 × 2000</span></div>{figure()}{downloads()}</section>
<div class="st-compose"><section id="copy"><div class="st-panel-head"><h2>Post copy</h2><span>Editable</span></div>{editor('headline', headline, 3, 'Copy headline')}{editor('post-text', post, 20, 'Copy full post')}</section><section id="accessibility"><div class="st-panel-head"><h2>Image alt text</h2><span>Accessibility</span></div>{editor('alt-text', alt, 8, 'Copy image alt text')}</section></div></div></main><footer class="st-footer">Local comparison only · No LinkedIn publication</footer>"""


pages = {
    "editorial.html": shell("Editorial", "editorial", editorial),
    "control-room.html": shell("Control Room", "control", control),
    "studio.html": shell("Materials Studio", "studio", studio),
}
for filename, content in pages.items():
    (HERE / filename).write_text(content)
print("Built:", ", ".join(pages))
