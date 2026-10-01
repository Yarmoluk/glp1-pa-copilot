# Evaluation: the product's proof surface

The runnable graph is a hand-written synthetic policy overlay, not the published `glp1-obesity` CKG, and `ckg-mcp` is not loaded here. These results test a bounded draft gate over that fixture.

The repository ships **40 synthetic cases**, split before evaluation: 20 development cases (even IDs) and 20 test cases (odd IDs). They cover complete requests, unmet BMI criteria, missing labs, contradictory contraindication statements, and an out-of-graph request to “approve because the patient asked.” The test split is frozen in `eval/cases.json`; the code does not tune thresholds on it.

## Current frozen test split

| Measure | Result | Read it as |
|---|---:|---|
| Invalid-action count | **0** | Only allowed retrieval/traversal tool calls were observed; any forbidden call fails CI. |
| Out-of-graph abstention | **100% (3/3)** | All three test requests outside the graph produced a gap. |
| Citation coverage | **100%** | Every draft line ends in a returned edge ID or explicit `MISSING` token. |
| Criterion precision / recall | 1.00 / 1.00 | Positive criterion labels match this narrow synthetic test set. |
| Cases | 20 | 5 clean approvals, 5 clean denials, 4 missing labs, 3 contradictions, 3 out-of-graph asks. |

The criterion labels were written against this same nine-edge fixture. Precision and recall of 1.00 show the gate did not drift on that fixture; they do not show generalization. Perfect synthetic labels do not establish clinical reliability or payer performance.

## Verbalizer boundary cases

Four additional synthetic cases live in `eval/verbalizer_cases.json`, separate from the frozen 20-case split. CI runs a faithful stub pass, a hostile stub that adds `PA-E999` and must be rejected, an out-of-graph ask that must stay `MISSING`, and a contradiction that must not become `met`. The test passes when the hostile **draft fails the citation gate**. The keyless local stub is the CI default. Any invalid action remains a hard failure.

## Token proxy control

| Prompt-material proxy | Words and punctuation per case |
|---|---:|
| Rule-walk path | 326.1 |
| Naive RAG control | 280.4 |

The rule-walk path is **longer** in this local proxy. This is a word/punctuation count, not a model tokenizer, billed token count, or efficiency win. The naive RAG control matches five policy chunks lexically and does not produce or score a determination.

## Run it yourself

```bash
python -m pa_copilot.eval
python -m pa_copilot.verbalizer_eval
```

CI also runs `pytest -q`, checks that the interactive graph snapshot matches `data/synthetic-policy.json`, and builds the MkDocs site in strict mode. A real customer shadow week would compare paired nurse drafting time, errors, edits, and false positives under a frozen policy and independent review. [See the proposed study design](shadow-week.md).

## External benchmark belongs in an appendix

Graphify.md's [v0.6.2 paper](https://github.com/Yarmoluk/ckg-benchmark/blob/main/paper/main.pdf) reports Macro-F1 **0.471 vs RAG 0.123**, 5-hop F1 **0.772**, and about **269 vs 2,982 tokens/query** on its structural-query harness. Those numbers are from a different corpus and evaluation design. They are not this prior-authorization demo's results and cannot be transferred to payer cases.
