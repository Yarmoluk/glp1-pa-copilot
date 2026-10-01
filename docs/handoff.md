# Customer engineer handoff

The only authorization rules live in `data/synthetic-policy.json`. Each criterion has a stable edge ID, predicate, source URL, and reviewed rationale. To change a criterion: obtain the signed current policy; add or version the edge and source; update the matching evaluator branch and synthetic cases; run `python -m pa_copilot.eval`; inspect the criterion precision/recall and abstentions; obtain clinical/policy-owner sign-off; release a new graph version. Never edit a source URL to disguise changed meaning. Removing an edge must make the service abstain. The bundled descriptive CKG is a navigation layer only.

Do not enter PHI into the public demo. `AUDIT_PATH` defaults to a local file; the append-only JSONL log is illustrative, not a production tamper-evident store. A production handoff would need identity, retention, access, policy-version approval, PHI controls, and external-system integration review.
