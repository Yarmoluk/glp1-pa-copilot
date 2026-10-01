"""Build the local warm editorial alternative from the existing materials."""
from pathlib import Path
import re
HERE = Path(__file__).resolve().parent
palette = dict(zip(
['#071b27','#0c2933','#103b40','#12333e','#123942','#194e50','#253b3a','#326069','#392c33','#6de6c4','#a18a53','#b67778','#d5e5e5','#f1ac9e','#f1c57b','#f1f6ed'],
['#faf6ee','#fffdf8','#faf6ee','#fffdf8','#f3eadc','#efe0ce','#f0e8d8','#c5b7a2','#f9e7e1','#99472e','#927137','#ae6253','#5c554b','#9e3829','#785719','#26241f']))
svg=(HERE.parent/'linkedin-graph.svg').read_text()
svg=re.sub(r'#[0-9a-fA-F]{6}',lambda m:palette.get(m[0],m[0]),svg)
# Keep the illustration focused on the walk, gate, and results.
import xml.etree.ElementTree as ET
ET.register_namespace('', 'http://www.w3.org/2000/svg')
root = ET.fromstring(svg)
for parent in root.iter():
    for node in list(parent):
        tag = node.tag.rsplit('}', 1)[-1]
        y = float(node.get('y', '0'))
        if (tag == 'text' and (y == 82 or y >= 1690)) or (tag == 'path' and node.get('d') == 'M80 1830H1520'):
            parent.remove(node)
        elif tag == 'text' and y == 335:
            node.text = 'GLP-1 prior-authorization draft gate'
root.set('viewBox', '0 100 1600 1580')
root.set('height', '1580')
svg = ET.tostring(root, encoding='unicode')
(HERE/'warm-graph.svg').write_text(svg)
html=(HERE/'editorial.html').read_text().replace('class="editorial"','class="editorial warm"').replace('href="styles.css"','href="styles.css"><link rel="stylesheet" href="warm.css"').replace('Editorial ·','Warm Editorial ·').replace('#eef2ef','#faf6ee')
html=html.replace('../linkedin-graph.png','warm-graph.png').replace('../linkedin-graph.svg','warm-graph.svg')
html=html.replace('A LinkedIn post, a traceable graph, and the words needed to publish them accurately.','A small, synthetic demonstration of a big design decision: every claim needs a declared relationship behind it.')
html=html.replace('<h1>A model can write.','<p class="eyebrow">FIELD NOTES / 01 &nbsp; — &nbsp; SYNTHETIC DEMONSTRATION</p><h1>A model can write.')
html=html.replace('Edit the text here, then copy the version you want to publish.','Working copy for review. Edits in these fields last for this browser session.')
html=re.sub(r'<figcaption>.*?</figcaption>', '', html, flags=re.S)
html=html.replace('width="1600" height="2000"', 'width="1600" height="1580"').replace('1600 × 2000', '1600 × 1580')
(HERE/'warm-editorial.html').write_text(html)
import cairosvg
cairosvg.svg2png(bytestring=svg.encode(),write_to=str(HERE/'warm-graph.png'))
print('Built warm editorial page and light SVG/PNG.')
