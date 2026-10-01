# Action boundary

| Stage | Allowed | Forbidden |
|---|---|---|
| Intake | Parse submitted synthetic case fields; preserve missing values | Infer diagnosis or fabricate evidence |
| Graph | Retrieve anchors, traverse declared policy edges, check contradictions | Add an edge at runtime or substitute model memory |
| Draft | Verbalize returned paths; flag gaps with `MISSING` | Invent a citation or make a final benefit decision |
| Review | Named reviewer accepts or edits a local draft; record diff | Submit to a payer, message a prescriber, or set an approval bit |

**Walk → optional verbalize → human accept/edit.** The rule walk is the source of truth: it returns edge IDs, `met`/`not_met`/`missing` outcomes, gaps, and contradictions. The optional verbalizer may word only those results. It cannot add an edge or turn a contradiction into `met`; a fabricated edge makes the entire draft fail before it can enter `pending_review`.

Every draft sentence ends with one or more returned edge IDs or `MISSING`. Review remains `pending_review` until the reviewer endpoint records acceptance or an edit. The endpoint changes *draft review status only*. It has no claim-submission integration and no approval field. Audit events are append-only JSONL with case ID, tool calls, edge IDs, renderer ID (`rule-walk-v1`, `verbalizer-stub-v1`, or `verbalizer-live`), reviewer ID where applicable, and UTC timestamps. The UI's Submit control is disabled by design.

## Do not automate yet

1. **Appeal filing:** low reversibility after an external submission; payer and member rights need careful handling. Volume is unknown, so there is no demonstrated automation return.
2. **Peer-to-peer scheduling:** contacting clinicians and handling availability reaches outside the authorized data rights and communications boundary. A mistaken message is hard to retract; volume is unmeasured.
3. **Diagnosis inference:** inferring an unsubmitted diagnosis from labs or notes creates a clinically consequential claim and may use information beyond the payer's rights. Reviewers must supply and verify diagnoses; volume does not justify this risk.
