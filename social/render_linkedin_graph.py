"""Render the actual synthetic fixture topology as a LinkedIn graphic."""
from pathlib import Path
import json
from html import escape
import cairosvg

ROOT = Path(__file__).resolve().parents[1]
policy = json.loads((ROOT / 'data/synthetic-policy.json').read_text())
parts = ['''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="2000" viewBox="0 0 1600 2000"><title>The model can write. It cannot invent an edge.</title><desc>Nine declared requires edges from the synthetic GLP-1 policy fixture, followed by an optional verbalizer, citation gate and human review. A fabricated edge is rejected.</desc><defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#071b27"/><stop offset="1" stop-color="#103b40"/></linearGradient><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 1L7 4L0 7" fill="none" stroke="#6de6c4" stroke-width="1.3"/></marker></defs><rect width="1600" height="2000" fill="url(#bg)"/><circle cx="1490" cy="100" r="470" fill="#6de6c4" opacity=".025"/><g font-family="Arial, Helvetica, sans-serif">''']
def text(x,y,s,size=24,color='#d5e5e5',weight=400):
 parts.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(s)}</text>')
def box(x,y,w,h,fill='#123942',stroke='#326069',r=16):
 parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
def path(d,color='#6de6c4',arrow=True):
 parts.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="3" opacity=".8"'+(' marker-end="url(#arrow)"' if arrow else '')+'/>')
text(80,82,'DANIEL YARMOLUK  /  FORWARD DEPLOYED ENGINEERING',22,'#6de6c4',700)
text(80,184,'The model can write.',80,'#f1f6ed',700)
text(80,276,'It cannot invent an edge.',80,'#f1f6ed',700)
text(80,335,'GLP-1 prior-authorization draft gate · Synthetic portfolio engagement',28)
parts.append('<path d="M80 374H1520" stroke="#326069"/>')
text(80,420,'01  WALK THE DECLARED GRAPH',22,'#6de6c4',700)
text(80,462,'Actual fixture topology',24,'#f1f6ed',700)
text(80,497,'Every arrow means “requires”.',21)
positions={'wegovy_start':(80,800,300,140), 'adult_weight_management':(650,540,370,80), 'bmi_30_or_27_with_comorbidity':(1170,540,350,80)}
labels={'adult_weight_management':('Adult weight-management','scope'), 'bmi_30_or_27_with_comorbidity':('BMI criterion','with comorbidity branch'), 'dose_0_25_weekly':('Starting dose','0.25 mg weekly'), 'lifestyle_program_documented':('Lifestyle program','documented'), 'prior_therapy_documented':('Prior therapy','or documented exception'), 'no_label_contraindication':('Contraindications','submitted safety check'), 'no_concurrent_glp1':('Concurrent GLP-1 therapy','combination check'), 'renal_value_documented':('eGFR documented','No cutoff encoded'), 'a1c_documented':('A1c documented','No eligibility cutoff')}
for i,key in enumerate(list(labels)[2:]): positions[key]=(650,650+i*110,370,80)
for edge in policy['edges']:
 sx,sy,sw,sh=positions[edge['from']]; tx,ty,tw,th=positions[edge['to']]
 start=(sx+sw,sy+sh/2); end=(tx,ty+th/2)
 if edge['id']=='PA-E02':
  path(f'M{start[0]} {start[1]} H{end[0]-8}')
  text(1045,565,edge['id'],20,'#6de6c4',700)
 else:
  path(f'M{start[0]} {start[1]} C490 {start[1]} 500 {end[1]} {end[0]-8} {end[1]}')
  text(545,end[1]-13,edge['id'],20,'#6de6c4',700)
for key,(x,y,w,h) in positions.items():
 box(x,y,w,h,fill='#194e50' if key=='wegovy_start' else '#12333e',stroke='#6de6c4' if key=='wegovy_start' else '#326069')
 if key=='wegovy_start':
  text(x+24,y+43,'SYNTHETIC REQUEST',18,'#6de6c4',700)
  text(x+24,y+83,'Wegovy start',32,'#f1f6ed',700)
  text(x+24,y+117,'Rule walk begins here',20)
 else:
  a,b=labels[key]; text(x+20,y+33,a,23,'#f1f6ed',700);text(x+20,y+61,b,20)
box(80,1030,330,180,fill='#253b3a',stroke='#a18a53')
text(104,1070,'NO SUPPORTING EDGE?',20,'#f1c57b',700)
text(104,1120,'MISSING',39,'#f1c57b',700)
text(104,1160,'A visible gap for the reviewer.',20)
text(1120,707,'02  WORD THE RETURNED PATH',20,'#6de6c4',700)
box(1120,732,400,105)
text(1144,772,'Optional verbalizer',27,'#f1f6ed',700)
text(1144,806,'Receives rule-walk results only',20)
path('M1320 843V877')
box(1120,888,400,105)
text(1144,928,'Citation + outcome gate',26,'#f1f6ed',700)
text(1144,962,'Returned edge IDs or MISSING',20)
box(1120,1012,400,92,fill='#392c33',stroke='#b67778')
text(1144,1049,'HOSTILE STUB TEST',18,'#f1ac9e',700)
text(1144,1083,'PA-E999 invented → REJECTED',22,'#f1ac9e',700)
text(1120,1170,'03  HUMAN ACCEPTS OR EDITS',20,'#6de6c4',700)
box(1120,1195,400,135,fill='#194e50',stroke='#6de6c4')
text(1144,1235,'pending_review',29,'#f1f6ed',700)
text(1144,1270,'Named reviewer · edit diff logged',20)
text(1144,1304,'Submit remains blocked',22,'#6de6c4',700)
text(80,1438,'FROZEN SYNTHETIC TEST SPLIT · 20 CASES',22,'#6de6c4',700)
for x,value,label in [(80,'0','invalid actions'),(570,'3 / 3','out-of-graph asks abstained'),(1060,'100%','citation coverage')]:
 box(x,1470,460,165,fill='#0c2933')
 text(x+28,1545,value,58,'#f1f6ed',700);text(x+28,1595,label,23)
text(80,1690,'Hand-written nine-edge synthetic policy overlay.',26,'#f1f6ed',700)
text(80,1730,'The published glp1-obesity CKG and ckg-mcp are not loaded here.',24)
text(80,1770,'Fixture results demonstrate gate behavior; they do not establish generalization.',23)
parts.append('<path d="M80 1830H1520" stroke="#326069"/>')
text(80,1887,'EXPLORE THE GRAPH. CLONE THE REPO. TEST THE BOUNDARY.',23,'#6de6c4',700)
text(80,1936,'yarmoluk.github.io/glp1-pa-copilot',30,'#f1f6ed',700)
parts.append('</g></svg>')
svg=''.join(parts)
out=ROOT/'social/linkedin-graph.svg';out.write_text(svg)
cairosvg.svg2png(bytestring=svg.encode(),write_to=str(out.with_suffix('.png')))
print(out.with_suffix('.png'))
