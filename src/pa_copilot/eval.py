"""Frozen synthetic evaluation. Test cases are never used for threshold tuning."""
from __future__ import annotations
import json
import re
from pathlib import Path
from .core import Graph, ROOT, evaluate, render

WORD = re.compile(r"\w+|[^\w\s]", re.UNICODE)
def tokens(text: str) -> int:
    """Deterministic lexical-token proxy, not a model tokenizer."""
    return len(WORD.findall(text))

def naive_rag_control(case: dict, graph: Graph) -> str:
    """Simple lexical top-k policy-chunk retrieval; no generation or correctness claim."""
    query = " ".join(str(v) for v in case.values() if v is not None)
    q = set(w.lower() for w in WORD.findall(query) if w.isalpha())
    chunks = [f"{e['id']} {e['from']} {e['to']} {e['rationale']} Source: {e['source']}" for e in graph.edges.values()]
    ranked = sorted(chunks, key=lambda s: len(q & set(w.lower() for w in WORD.findall(s) if w.isalpha())), reverse=True)
    return query + "\n" + "\n".join(ranked[:5])

def run(split: str = "test", graph: Graph | None = None) -> dict:
    graph = graph or Graph()
    rows = json.loads((ROOT / "eval/cases.json").read_text())
    rows = [r for r in rows if r["split"] == split]
    tp=fp=fn=covered=sentences=out_total=out_abstained=invalid=0
    graph_tokens=rag_tokens=0
    by_kind={}
    for row in rows:
        results, calls = evaluate(row["case"], graph)
        draft, disposition, gaps = render(results)
        predicted={r.criterion:r.outcome for r in results}
        expected=row["expected"]
        for key in set(expected)|set(predicted):
            truth=expected.get(key)=="met"
            pred=predicted.get(key)=="met"
            tp+=int(truth and pred);fp+=int(pred and not truth);fn+=int(truth and not pred)
        for line in draft.splitlines():
            sentences+=1
            covered+=int(bool(re.search(r"\[(?:PA-E\d{2}(?:,PA-E\d{2})*|MISSING)\]$",line)))
        if row["kind"]=="out_of_graph":
            out_total+=1;out_abstained+=int("out_of_graph_request" in gaps and disposition=="needs_information")
        # Action boundary is checked against the actual output schema and audit-independent evaluator.
        invalid+=sum(call not in {"validate_ckg", "traverse:wegovy_start"} for call in calls)
        graph_tokens+=tokens(" ".join(e["rationale"] for e in graph.traverse())+" "+draft)
        rag_tokens+=tokens(naive_rag_control(row["case"],graph))
        by_kind[row["kind"]]=by_kind.get(row["kind"],0)+1
    p=tp/(tp+fp) if tp+fp else 0
    recall=tp/(tp+fn) if tp+fn else 0
    return {"split":split,"cases":len(rows),"case_mix":by_kind,"citation_coverage":covered/sentences if sentences else 0,
            "out_of_graph_abstention_rate":out_abstained/out_total if out_total else 0,
            "criterion_precision":p,"criterion_recall":recall,"invalid_action_count":invalid,
            "lexical_tokens_per_case_graph":round(graph_tokens/len(rows),1),"lexical_tokens_per_case_naive_rag":round(rag_tokens/len(rows),1),
            "token_note":"Lexical-token proxy counts case+top-5 policy chunks for RAG; graph count includes traversed edge rationales+draft. No LLM call or billed-token claim."}

if __name__=="__main__":
    result=run("test")
    print(json.dumps(result,indent=2))
    if result["invalid_action_count"]:
        raise SystemExit(1)
