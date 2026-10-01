# What this public demo shows

**This is an illustration of consuming declared relationships, not a release of Graphify.md's CKG creation process.** The repo contains a small, hand-specified fictional payer policy fixture (`data/synthetic-policy.json`), generic traversal and rule checks, a draft renderer, a reviewer gate, and synthetic evaluation cases. The interactive graphic displays two selected edges from that same fixture.

It contains **no** document ingestion, concept discovery, relationship extraction, deduplication, compression, source-hash generation, graph construction pipeline, or Graphify.md engine implementation. The `glp1-obesity` CKG available through the separate public `ckg-mcp` package informed the discovery map, but this runnable demo does not load or redistribute that domain. The source links in the fictional policy illustrate reviewability; they are not a customer policy or proof that these synthetic rules apply to any plan.

The public code necessarily shows how this **example consumer** reads a tiny declared edge list and stops when an edge or submitted field is missing. It does not explain how Graphify.md produces a CKG from source material. The default `rule-walk-v1` renderer makes no model call; the optional verbalizer can word only returned results and cannot add an edge.

For a real engagement, a customer would provide an authorized, current, reviewed policy graph through a separate controlled process. This repository makes no claim that such a graph has been built or deployed.
