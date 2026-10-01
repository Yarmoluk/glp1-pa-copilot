"""Local research-style post kit; source content and actual fixture topology preserved."""
from pathlib import Path
from html import escape
import re
import cairosvg
P=Path(__file__).resolve().parent
source=(P.parent/'linkedin-post.md').read_text()
headline=source.split('# Headline\n')[1].split('# Post')[0].strip()
post=source.split('# Post\n')[1].split('# Image alt text')[0].strip()
alt=source.split('# Image alt text\n')[1].strip()
colors={'#faf6ee':'#ffffff','#fffdf8':'#ffffff','#f3eadc':'#f5f7fb','#efe0ce':'#eef1fb','#f0e8d8':'#fff8eb','#c5b7a2':'#c5cddd','#f9e7e1':'#fff0ec','#99472e':'#4859a0','#927137':'#876622','#ae6253':'#c65843','#5c554b':'#58616d','#9e3829':'#b33f2c','#785719':'#876622','#26241f':'#11171d'}
svg=(P/'warm-graph.svg').read_text()
svg=re.sub(r'#[0-9a-fA-F]{6}',lambda m:colors.get(m[0],m[0]),svg)
svg=svg.replace('rx="16"','rx="4"')
import xml.etree.ElementTree as ET
ET.register_namespace('', 'http://www.w3.org/2000/svg')
root=ET.fromstring(svg)
for node in root.iter():
    tag=node.tag.rsplit('}',1)[-1]
    if tag in ('g','text'):
        node.set('font-family','Arial, Helvetica, sans-serif')
    if tag!='text': continue
    # Use the original artwork's real regular/bold faces, without synthesized medium weights.
    if node.get('fill')=='#58616d':node.set('fill','#414c59')
    if re.fullmatch(r'PA-E\d+',node.text or ''):
        node.set('paint-order','stroke');node.set('stroke','#ffffff');node.set('stroke-width','7');node.set('stroke-linejoin','round')
svg=ET.tostring(root,encoding='unicode')
(P/'research-graph.svg').write_text(svg)
cairosvg.svg2png(bytestring=svg.encode(),write_to=str(P/'research-graph.png'))
def field(id,label,text,rows):
 return f'<div class="field"><div class="field-top"><label for="{id}">{label}</label><button data-copy="{id}">Copy {label.lower()} ↗</button></div><textarea id="{id}" rows="{rows}">{escape(text)}</textarea></div>'
html='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Trace the rule · Local post study</title><link rel="stylesheet" href="research.css"></head><body>
<a class="skip" href="#main">Skip to content</a>
<header><a href="comparison.html" class="brand"><span class="mark">⊞</span> GRAPH NOTES</a><nav aria-label="Materials"><a href="#graph">Diagram</a><a href="#copy">Post copy</a><a href="comparison.html">All designs ↗</a></nav><span class="draft">LOCAL DRAFT</span></header>
<main id="main"><section class="hero"><div class="network" aria-hidden="true"><svg viewBox="0 0 1000 450" preserveAspectRatio="xMidYMid slice"><g stroke="#d8ddef" stroke-width="1" fill="none"><path d="M40 370L190 110L365 280L520 50L660 230L870 100L960 360L660 230L510 410L365 280L40 370M190 110L520 50M365 280L660 230M870 100L520 50"/></g><g fill="#ced5ef"><rect x="185" y="105" width="10" height="10"/><rect x="360" y="275" width="10" height="10"/><rect x="515" y="45" width="10" height="10"/><rect x="865" y="95" width="10" height="10"/></g><rect x="653" y="223" width="14" height="14" fill="#efb0a5"/></svg></div><p class="kicker">01 / AGENT BOUNDARIES / SYNTHETIC DEMO</p><h1>Trace the rule.<br>Inspect the draft.<br><span>Keep the decision human.</span></h1><p class="intro">An inspectable boundary for GLP-1 prior-authorization drafting. Follow the declared criteria, see the gaps, and check where the model must stop.</p><a class="cta" href="#graph">EXPLORE THE DIAGRAM <span>↓</span></a></section>
<section class="flow" aria-label="Workflow"><div><span>01 / RETRIEVE</span><h2>Walk declared edges.</h2><p>The rule walk returns criteria results and missing evidence.</p></div><div><span>02 / CONSTRAIN</span><h2>Check the wording.</h2><p>An optional verbalizer uses the returned path. A fabricated edge is rejected.</p></div><div><span>03 / REVIEW</span><h2>Leave control with a person.</h2><p>A reviewer accepts or edits the draft. Submission stays blocked.</p></div></section>
<section id="graph" class="diagram"><div class="section-heading"><div><p class="kicker">THE ARTIFACT</p><h2>A boundary you can inspect.</h2></div><div class="downloads"><a href="research-graph.png" download>DOWNLOAD PNG ↗</a><a href="research-graph.svg" download>EDITABLE SVG ↗</a></div></div><img src="research-graph.svg" width="1600" height="1580" alt="'''+escape(alt,quote=True)+'''" loading="lazy"></section>
<section id="copy" class="copy"><div class="section-heading"><div><p class="kicker">THE POST</p><h2>Words to go with the work.</h2></div><p>Editable working copy.<br>Changes save in this browser.</p></div>'''+field('headline','Headline',headline,3)+field('post-text','Post',post,20)+field('alt-text','Image description',alt,5)+'''<button id="restore">Restore original copy</button></section></main><footer><span>LOCAL DESIGN STUDY / NOT PUBLISHED</span><span>White space. Declared paths. Human review.</span></footer><div id="copy-status" role="status" aria-live="polite" class="sr-only"></div><script src="app.js"></script><script>
const fields=[...document.querySelectorAll('textarea')];const originals=fields.map(f=>f.value);fields.forEach(f=>{try{const v=localStorage.getItem('research-post:'+f.id);if(v!==null)f.value=v}catch{}f.addEventListener('input',()=>{try{localStorage.setItem('research-post:'+f.id,f.value)}catch{document.getElementById('copy-status').textContent='Browser storage unavailable; copy your edits before closing.'}})});document.getElementById('restore').onclick=()=>{if(!confirm('Restore the original copy and discard edits in this design?'))return;fields.forEach((f,i)=>{f.value=originals[i];try{localStorage.removeItem('research-post:'+f.id)}catch{}})};
</script></body></html>'''
(P/'research.html').write_text(html)
p=P/'comparison.html';s=p.read_text()
if 'href="research.html"' not in s:
 s=s.replace('<main id="main" class="cmp-main">','<main id="main" class="cmp-main"><article><div class="cmp-copy"><span>E / Research notes · New</span><h2>Trace the rule. Inspect the draft.</h2><p>DataLab-inspired white space, monospaced labels, a subtle network, and coral accents.</p><a href="research.html">Open research design</a></div><iframe title="Research design preview" src="research.html" loading="lazy"></iframe></article>')
p.write_text(s)
print('Built local research post kit and SVG/PNG.')
