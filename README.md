# GLP-1 prior-authorization draft copilot

**Synthetic regional payer. Synthetic cases. Human review required.** A utilization-review nurse can inspect a declared criterion path, a cited draft, and explicit gaps. There is no submit, prescriber-message, or approval action.

Graphify.md compiles the documents an organization already trusts into a compressed knowledge graph so an agent can answer from declared relationships. This demo puts **domain graph first, model second**: a deterministic template verbalizes only traversed edges. [Graphify.md](https://graphifymd.com) exposes a model-agnostic [MCP endpoint](https://www.graphifymd.com/api/mcp) with `query_ckg`, `get_prerequisites`, `traverse`, and `validate_ckg`; this clone uses a thin offline adapter over the MIT-licensed `glp1-obesity` domain from [`ckg-mcp`](https://github.com/Yarmoluk/ckg-mcp) plus an explicit synthetic policy overlay. The descriptive bundled domain does **not** contain the PA thresholds.

![Browser view of a synthetic case, traversed criteria, gaps, and cited draft](docs/demo.png)

## Run in about 90 seconds

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e '.[test]'
uvicorn pa_copilot.api:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000`. Click **Draft from graph** for the happy path. For a fail-closed path, change `case_id` to `demo-002`, delete the `egfr` field, and click again. The second draft shows `PA-E08` as missing and its disposition is `needs_information`. The **Submit blocked** button stays disabled. Enter a reviewer ID to accept the draft locally; the append-only event appears in `audit.jsonl`.

```bash
pytest -q
python -m pa_copilot.eval
```

The UI accepts only synthetic examples. Do not paste patient information into the public demo.

## What the reviewer sees

`data/glp1-obesity.csv` contains the bundled domain's descriptive concepts. `data/synthetic-policy.json` declares nine fictional authorization and intake edges, each with a source-pattern URL. The deterministic BFS traversal returns those edges in stable order. Missing edge, missing submitted evidence, contradictory contraindication statements, or a request outside the graph produces `MISSING` and `needs_information`. A failed criterion with complete evidence produces `criteria_not_met`; all met produces `eligible_for_review`. None is a benefit decision. Every draft line ends in an edge ID or `MISSING`.

The default verbalizer is `deterministic-template-v1` and uses no model API. A model could replace that renderer only if it received the same path objects and passed the citation validator. Review acceptance changes draft status from `pending_review` to `reviewed_accepted` or `reviewed_edit`; it does not set an approval bit. Audit events contain case ID, tool calls, edge IDs, model ID, reviewer ID, UTC timestamp, and review diff. This local JSONL log illustrates the contract, not production tamper evidence.

## Frozen synthetic evaluation

The committed 40 cases contain 10 clean approvals, 10 clean denials, 8 missing labs, 6 contradictory contraindication statements, and 6 out-of-graph asks. Even IDs are development; odd IDs are the frozen test split. No test split tuning is performed. Current test results from `python -m pa_copilot.eval`:

| Metric | Result | Meaning |
|---|---:|---|
| Test cases | 20 | 5 approvals, 5 denials, 4 missing labs, 3 contradictions, 3 out-of-graph |
| Citation coverage | 100% | Draft lines end in returned edge ID or `MISSING` |
| Out-of-graph abstention | 100% | All three test asks become explicit gaps |
| Criterion precision / recall | 1.00 / 1.00 | Positive criterion classification on frozen synthetic labels |
| Invalid-action count | **0** | CI fails if an evaluator tool call leaves the allowed retrieve/traverse set |
| Graph lexical tokens / case | 326.1 | Edge rationales plus rendered draft |
| Naive RAG lexical tokens / case | 280.4 | Case plus lexical top-five policy chunks |

Token counts are a **lexical proxy**, not billed LLM tokens. The graph path is longer than this deliberately small retrieval control; this local test does not demonstrate token savings. The RAG control measures prompt material only and is not an answer-quality comparator. Perfect synthetic labels reflect a narrow fixture, not clinical reliability. A customer shadow week would measure review time and error rates on an approved corpus ([plan](docs/shadow-week.md)).

## Recruiter reading path

1. [Discovery and source mapping](docs/discovery.md)
2. [Action boundary and do-not-automate memo](docs/action-boundary.md)
3. [Why declared graph edges](docs/adr-001-graph-not-rag.md)
4. [Shadow-week measurement plan](docs/shadow-week.md)
5. [Criterion handoff](docs/handoff.md)

## Published benchmark context (separate appendix)

Graphify.md's [public v0.6.2 paper](https://github.com/Yarmoluk/ckg-benchmark/blob/main/paper/main.pdf) and [harness](https://github.com/Yarmoluk/ckg-benchmark) report Macro-F1 **0.471 vs RAG 0.123**, 5-hop F1 **0.772**, and roughly **269 vs 2,982 tokens/query** on their structural-query benchmark. Those are **not** results from this PA demo and should not be transferred to payer cases. Every answer in the CKG mechanism traces to a declared edge; that does not certify the edge as correct or current.

```text
335 domain queries
= 1,000,000 tokens · RAG
= 90,000 tokens · RAG + CKG
```

The context-window illustration is product positioning, not a measurement in this repo. Enterprise-agent context is often described as roughly 25% rules, 30% orchestration, 30% retrieved chunks and 15% domain; this engagement explores the inversion by loading a domain graph before any model verbalization.
