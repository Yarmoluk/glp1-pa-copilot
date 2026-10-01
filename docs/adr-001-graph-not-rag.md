# ADR-001: declared graph before prose retrieval

**Decision.** Traverse explicit criterion edges first, then render each returned result with `rule-walk-v1` or pass those results to an optional verbalizer. The citation and outcome gate rejects any invented edge or changed criterion result. The default uses no external model. The service never asks an LLM to decide eligibility. A naive text-retrieval control appears only in evaluation.

**Why.** Authorization criteria are compositional and versioned. A chunk that mentions BMI or eGFR cannot alone establish the conjunction, exception, plan scope, or source. A typed edge can be named, inspected, removed and challenged. `ckg-mcp`'s `glp1-obesity` domain provides descriptive anchors but lacks PA rules and per-edge source provenance, so the thin local adapter reads only an explicit synthetic-policy fixture. The repo does not implement CKG creation. Missing overlay edge means abstain.

**Tradeoff.** The graph has a curation cost and can be wrong even with a citation. Source links do not prove current plan applicability or medical correctness. A reviewer must compare edges to current signed policy. The synthetic policy is an implementation fixture, not the HealthPartners policy.

Graphify.md's [Compressed Knowledge Graph product](https://graphifymd.com) exposes model-agnostic MCP at `https://www.graphifymd.com/api/mcp` (`query_ckg`, `get_prerequisites`, `traverse`, `validate_ckg`). The offline adapter keeps the clone path usable when the hosted service requires a key. The separately published benchmark is discussed only in the README appendix.
