---
hide:
  - navigation
  - toc
---

# Explore the decision path

A graph edge is a named relationship. Click a scenario or a policy node below. The highlighted route shows what the service can cite—and where it must stop.

<div class="pa-graph-shell" id="pa-graph-explorer">
  <div class="pa-graph-toolbar" role="group" aria-label="Choose a synthetic case scenario">
    <button type="button" class="pa-scenario" data-scenario="supported" aria-pressed="true">Evidence present</button>
    <button type="button" class="pa-scenario" data-scenario="missing" aria-pressed="false">Lab missing</button>
    <button type="button" class="pa-scenario" data-scenario="outside" aria-pressed="false">No policy edge</button>
  </div>
  <p class="pa-swipe">Swipe the graph sideways to follow the path →</p>
  <div class="pa-graph-canvas" tabindex="0" aria-label="Scroll horizontally to view the full reasoning graph">
    <svg id="pa-decision-graph" viewBox="0 0 1010 430" role="img" aria-labelledby="pa-graph-title pa-graph-desc">
      <title id="pa-graph-title">Interactive prior-authorization reasoning graph</title>
      <desc id="pa-graph-desc">A synthetic case enters a policy root, branches to BMI, renal documentation, or a missing policy edge, then reaches a draft and a human reviewer. Choose a scenario to highlight a route.</desc>
      <g class="pa-graph-links" fill="none" stroke-linecap="round">
        <path d="M154 217H205" data-route="all"/><path d="M353 217C395 217 395 99 438 99" data-route="supported"/><path d="M353 217H438" data-route="missing"/><path d="M353 217C395 217 395 335 438 335" data-route="outside"/>
        <path d="M592 99C634 99 634 217 678 217" data-route="supported"/><path d="M592 217H678" data-route="missing"/><path d="M592 335C634 335 634 217 678 217" data-route="outside"/><path d="M822 217H865" data-route="all"/>
      </g>
      <g class="pa-graph-node pa-node-case" transform="translate(20 173)"><rect width="134" height="88" rx="16"/><text x="20" y="34" class="pa-node-kicker">INPUT</text><text x="20" y="62" class="pa-node-title">Case facts</text></g>
      <g class="pa-graph-node pa-node-root" transform="translate(205 173)"><rect width="148" height="88" rx="16"/><text x="20" y="34" class="pa-node-kicker">TRAVERSE</text><text x="20" y="62" class="pa-node-title">Policy graph</text></g>
      <g class="pa-graph-node pa-node-branch" data-node="supported" transform="translate(438 55)" role="button" tabindex="0" aria-label="Inspect BMI edge PA-E02"><rect width="154" height="88" rx="16"/><text x="18" y="34" class="pa-node-kicker">DECLARED EDGE</text><text x="18" y="63" class="pa-node-title">PA-E02 · BMI</text></g>
      <g class="pa-graph-node pa-node-branch" data-node="missing" transform="translate(438 173)" role="button" tabindex="0" aria-label="Inspect renal documentation edge PA-E08"><rect width="154" height="88" rx="16"/><text x="18" y="34" class="pa-node-kicker">DECLARED EDGE</text><text x="18" y="63" class="pa-node-title">PA-E08 · eGFR</text></g>
      <g class="pa-graph-node pa-node-branch pa-node-gap" data-node="outside" transform="translate(438 291)" role="button" tabindex="0" aria-label="Inspect request with no policy edge"><rect width="154" height="88" rx="16"/><text x="18" y="34" class="pa-node-kicker">NO DECLARED EDGE</text><text x="18" y="63" class="pa-node-title">MISSING</text></g>
      <g class="pa-graph-node pa-node-draft" transform="translate(678 173)"><rect width="144" height="88" rx="16"/><text x="20" y="34" class="pa-node-kicker">OUTPUT</text><text x="20" y="62" class="pa-node-title">Cited draft</text></g>
      <g class="pa-graph-node pa-node-review" transform="translate(865 173)"><rect width="125" height="88" rx="16"/><text x="18" y="34" class="pa-node-kicker">STOP HERE</text><text x="18" y="62" class="pa-node-title">Nurse review</text></g>
    </svg>
  </div>
  <div class="pa-graph-detail" aria-live="polite">
    <div><p class="pa-detail-label">Submitted fact</p><p id="pa-fact"></p></div>
    <div><p class="pa-detail-label">Declared relationship</p><p id="pa-relationship"></p><a id="pa-source" target="_blank" rel="noopener noreferrer"></a></div>
    <div><p class="pa-detail-label">Draft excerpt</p><p id="pa-draft"></p></div>
  </div>
  <p class="pa-graph-note">This is a schematic of a <strong>hand-specified synthetic</strong> policy fixture, not a generated CKG. The full app checks nine criteria, not only the one highlighted here. The illustrated edge metadata is copied from <code>data/synthetic-policy.json</code>.</p>
</div>

## What changed when you clicked?

The case fact did not become an answer by itself. The service first had to find a declared edge. With evidence present, the draft can cite `PA-E02`. With eGFR omitted, `PA-E08` exists but its required submitted value is missing, so the draft records a gap. For an out-of-graph request such as “approve because the patient asked,” there is no matching edge at all; the graph cannot license that claim.

The [local demo](run.md) lets you paste these synthetic inputs into the local FastAPI service. The [engineering explanation](how-it-works.md) shows the code path and human gate.


This published context-window illustration is product positioning, not a token measurement from this demo. See the [local evaluation](evaluation.md) for measured lexical-token results.
