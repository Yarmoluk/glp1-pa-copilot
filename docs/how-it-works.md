# How the copilot works

## A five-step picture

```mermaid
graph LR
  A[Submitted synthetic case] --> B[Declared policy edges]
  B --> C[Deterministic checks]
  C --> D[Cited draft or explicit gap]
  D --> E[Named human reviewer]
```

The service loads **only a synthetic policy fixture**. The separate public `glp1-obesity` domain informed the discovery map, but it is not loaded or redistributed here. The fixture names the nine illustrative criteria the demo checks, from scope and BMI to dose, prior therapy, safety flags, and documentation fields. Each edge has a stable ID and a public source-pattern link. This consumer-side code does not create a CKG from documents.

For each case, a deterministic breadth-first traversal returns the reachable policy edges. The evaluator checks only those edges against submitted fields. If an edge is absent, a field is missing, the input contradicts itself, or a request has no matching edge, it emits a gap. The renderer writes only the result objects it receives. The default `model_id` is `deterministic-template-v1`: **no LLM call is made**. This makes the demo's action boundary easy to inspect.

## Follow one criterion

| Item | Value in the happy path |
|---|---|
| Submitted fact | BMI `33.2` |
| Declared policy relationship | `PA-E02`: adult weight-management request requires the BMI criterion |
| Deterministic result | `met` |
| Draft excerpt | `PA-E02: met; BMI threshold ... [PA-E02]` |
| Final action | Draft remains `pending_review` |

A source URL attached to an edge makes the rule inspectable; it does **not** make a fictional policy legally applicable or clinically current. A customer engineer would need a signed policy version and policy-owner attestation before using this pattern in a real workflow.

## Where the model cannot act

The code exposes `/cases/draft`, `/cases/{case_id}`, and `/cases/{case_id}/review`. It has **no submit endpoint** and no approval bit. A named reviewer may accept or edit a draft locally; the service logs the diff. Every rendered draft line ends in a returned edge ID or `MISSING`. The [action boundary](action-boundary.md) also explains why appeal filing, peer-to-peer scheduling, and diagnosis inference are outside scope.

## What is here, and what a real deployment needs

| In this repo | Needed for a real payer deployment |
|---|---|
| Synthetic policy overlay, source-pattern URLs | Signed, current plan policy and clinical/policy-owner review |
| Synthetic case JSON | Authorized intake, identity, access, PHI controls |
| Local append-only JSONL | Durable audit storage, retention, access control, tamper evidence |
| Local reviewer ID | Authenticated reviewer identity and separation of duties |
| Frozen synthetic evaluation | Shadow-week measurement on approved cases and independent human scoring |

[Read the architecture decision](adr-001-graph-not-rag.md) or [change a criterion safely](handoff.md).
