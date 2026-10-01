# Evaluation: the product's proof surface

The repository ships **40 synthetic cases**, split before evaluation: 20 development cases (even IDs) and 20 test cases (odd IDs). They cover complete requests, unmet BMI criteria, missing labs, contradictory contraindication statements, and an out-of-graph request to “approve because the patient asked.” The test split is frozen in `eval/cases.json`; the code does not tune thresholds on it.

## Current frozen test split

| Measure | Result | Read it as |
|---|---:|---|
| Cases | 20 | 5 clean approvals, 5 clean denials, 4 missing labs, 3 contradictions, 3 out-of-graph asks |
| Citation coverage | 100% | Every draft line ends in a returned edge ID or explicit `MISSING` token. |
| Out-of-graph abstention | 100% | All three test requests outside the graph produced a gap. |
| Criterion precision / recall | 1.00 / 1.00 | Positive criterion labels match this narrow synthetic test set. |
| Invalid-action count | **0** | Only allowed retrieval/traversal tool calls were observed; any forbidden call fails CI. |
| Graph lexical tokens per case | 326.1 | Traversed edge rationales plus the rendered draft. |
| Naive RAG lexical tokens per case | 280.4 | Case text plus five lexically matched policy chunks. |

The graph path is **longer** in this local token proxy. That is an honest result, not a token-efficiency claim. The naive RAG control is a prompt-material comparison only; it does not produce or score a determination. Token counts use a deterministic word/punctuation proxy, not a model tokenizer or billed tokens. Perfect synthetic labels do not establish clinical reliability or payer performance.

## Run it yourself

```bash
python -m pa_copilot.eval
```

CI also runs `pytest -q`, checks that the interactive graph snapshot matches `data/synthetic-policy.json`, and builds the MkDocs site in strict mode. A real customer shadow week would compare paired nurse drafting time, errors, edits, and false positives under a frozen policy and independent review. [See the proposed study design](shadow-week.md).

## External benchmark belongs in an appendix

Graphify.md's [v0.6.2 paper](https://github.com/Yarmoluk/ckg-benchmark/blob/main/paper/main.pdf) reports Macro-F1 **0.471 vs RAG 0.123**, 5-hop F1 **0.772**, and about **269 vs 2,982 tokens/query** on its structural-query harness. Those numbers are from a different corpus and evaluation design. They are not this prior-authorization demo's results and cannot be transferred to payer cases.
