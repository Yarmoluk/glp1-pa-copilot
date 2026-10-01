---
hide:
  - navigation
  - toc
---

<div class="pa-hero" markdown>
  <p class="pa-eyebrow">A FORWARD DEPLOYED ENGINEERING CASE STUDY</p>
  <h1>Can a draft explain exactly why it says what it says?</h1>
  <p class="pa-lead">A nurse receives a GLP-1 prior-authorization request. This synthetic copilot checks declared policy relationships, drafts a response with edge citations, and stops for human review.</p>
  <div class="pa-actions">
    <a class="pa-button pa-button-primary" href="graph/">Explore the interactive graph →</a>
    <a class="pa-button pa-button-secondary" href="run/">Clone and run the demo</a>
  </div>
  <p class="pa-hero-note">Fictional regional payer · Synthetic patient cases · No submissions</p>
</div>

![Illustrated path from case fact through declared policy edge to cited draft and nurse review](assets/hero.svg){ .pa-hero-art }

## The idea, without the jargon

A prior-authorization request is a question: **does this request meet this plan's rules, with enough evidence to say so?** A search tool can find paragraphs that *sound* relevant. This demo uses a small, explicit map of relationships instead. Each rule has an ID, a source pattern, and a place in the path from request to draft. If the map cannot support a sentence, the draft says `MISSING`.

Graphify.md calls its product a **Compressed Knowledge Graph (CKG)**. This page uses a tiny, hand-specified **illustrative policy graph** so you can see the consumer-side behavior. Here, “graph” simply means named things joined by declared relationships. A path such as *Wegovy start → requires → BMI criterion* is checkable. It is not a clinical diagnosis, a coverage decision, or a substitute for the nurse.

<div class="pa-card-grid" markdown>
<div class="pa-card" markdown>
### 01 · The request
A fictional adult starts Wegovy injection for weight management. The case includes dose, BMI, labs, prior treatment, and safety fields.
</div>
<div class="pa-card" markdown>
### 02 · The path
The service walks declared synthetic policy edges. It checks submitted facts against each criterion and names missing or contradictory evidence.
</div>
<div class="pa-card" markdown>
### 03 · The handoff
Every draft line ends in an edge ID or `MISSING`. A nurse can accept or edit the *draft review*; the app cannot submit or approve a request.
</div>
</div>

## One case, two outcomes

| Input | What the demo shows | Why it matters |
|---|---|---|
| BMI 33.2, start dose 0.25 mg, all required fields supplied | `eligible_for_review`, with `PA-E02` and other edge citations | A reviewer sees the exact policy path behind the draft. |
| Same case, eGFR omitted | `needs_information`, with `PA-E08` under Explicit gaps | The draft exposes the gap instead of filling it from a model's memory. |

`eligible_for_review` is a **draft disposition**, not a benefit approval. Both examples stay `pending_review` until a named reviewer acts locally. [Walk through them in the app](run.md), or [click the graph first](graph.md).

!!! note "What is real here?"
    The product concept, public FDA and payer source patterns, code, tests, and audit design are real. The payer, its policy graph, and all cases are synthetic. The private CKG creation process is not included. The demo is not a customer deployment or a clinical decision system.

## Where to go next

- **New to graphs?** [Explore one edge and one gap](graph.md).
- **Want to run it?** [Clone, start, and test two cases](run.md).
- **Evaluating the engineering?** [Read how the graph, reviewer gate, and audit log work](how-it-works.md), then inspect the [frozen evaluation](evaluation.md).
- **Assessing deployment judgment?** Read the [discovery note](discovery.md), [action boundary](action-boundary.md), and [handoff](handoff.md).
