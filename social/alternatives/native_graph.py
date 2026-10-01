"""Live HTML diagram. SVG is used only for measured connectors."""
from html import escape

def diagram(edges):
    labels={
      'adult_weight_management':('Adult weight-management','Scope'),
      'bmi_30_or_27_with_comorbidity':('BMI criterion','With comorbidity branch'),
      'dose_0_25_weekly':('Starting dose','0.25 mg weekly'),
      'lifestyle_program_documented':('Lifestyle program','Documented'),
      'prior_therapy_documented':('Prior therapy','Or documented exception'),
      'no_label_contraindication':('Contraindications','Submitted safety check'),
      'no_concurrent_glp1':('Concurrent GLP-1 therapy','Combination check'),
      'renal_value_documented':('eGFR documented','No cutoff encoded'),
      'a1c_documented':('A1c documented','No eligibility cutoff')}
    nodes=[]
    for e in edges:
        title,note=labels[e['to']]
        nodes.append(f'''<article class="ng-node ng-criterion {'ng-dependent' if e['id']=='PA-E02' else ''}" id="ng-{e['to']}" data-from="ng-{e['from']}"><a class="ng-edge" href="{escape(e['source'],quote=True)}" target="_blank" rel="noopener" aria-label="Inspect source for {e['id']}">{e['id']} <span>requires ↗</span></a><h3>{title}</h3><p>{note}</p></article>''')
    return '''<div class="native-graph" id="native-graph"><div class="ng-heading"><p class="kicker">01 / WALK THE DECLARED GRAPH</p><h2>Every criterion has a path.</h2><p>Nine declared relationships. Every arrow means “requires”.</p></div><div class="ng-map"><svg class="ng-lines" aria-hidden="true"><defs><marker id="ng-arrow" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="8" markerHeight="8" markerUnits="userSpaceOnUse" orient="auto"><path d="M 0 0 L 8 4 L 0 8 L 2 4 Z" fill="#667f9b" stroke="none"/></marker></defs><g class="ng-paths"></g></svg><article class="ng-node ng-request" id="ng-wegovy_start"><span class="ng-edge">SYNTHETIC REQUEST</span><h3>Wegovy start</h3><p>The rule walk begins here.</p></article>'''+''.join(nodes)+'''</div><div class="ng-gap"><strong>No supporting evidence?</strong><span><b>MISSING</b> stays visible for the reviewer.</span></div><div class="ng-workflow"><article><p class="kicker">02 / OPTIONAL VERBALIZER</p><h3>Word the returned path.</h3><p>Receives rule-walk results only.</p></article><article><p class="kicker">CITATION + OUTCOME GATE</p><h3>Reject invented edges.</h3><p>Returned edge IDs or MISSING.</p><span class="ng-reject">Hostile stub: PA-E999 → rejected</span></article><article><p class="kicker">03 / HUMAN REVIEW</p><h3>Accept or edit the draft.</h3><p>Named reviewer. Edit diff logged.</p><span class="ng-pending">pending_review · Submit blocked</span></article></div><div class="ng-results"><p class="kicker">FROZEN SYNTHETIC TEST SPLIT / 20 CASES</p><div><article><strong>0</strong><p>Invalid actions</p></article><article><strong>3 / 3</strong><p>Out-of-graph asks abstained</p></article><article><strong>100%</strong><p>Citation coverage</p></article></div></div></div>'''
