"""Separate frozen cases for the verbalizer boundary; no test-split tuning."""
from __future__ import annotations

import json
from .core import Graph, ROOT, evaluate
from .verbalizer import StubVerbalizer, citation_errors


def run() -> dict:
    cases = json.loads((ROOT / "eval/verbalizer_cases.json").read_text())
    graph = Graph()
    outcomes: list[dict] = []
    for row in cases:
        results, _ = evaluate(row["case"], graph)
        draft = StubVerbalizer(row["mode"]).verbalize(results)
        errors = citation_errors(draft, results)
        accepted = not errors
        passed = accepted == row["expect_accepted"]
        if row["name"] == "out_of_graph_missing":
            passed &= "out_of_graph_request: missing" in draft and "[MISSING]" in draft
        if row["name"] == "contradiction_not_met":
            passed &= "PA-E06: missing; contradictory" in draft and "PA-E06: met;" not in draft
        outcomes.append({"case": row["name"], "accepted": accepted, "expected": row["expect_accepted"], "passed": bool(passed)})
    return {"cases": len(outcomes), "passed": sum(row["passed"] for row in outcomes), "results": outcomes}


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2))
    if result["passed"] != result["cases"]:
        raise SystemExit(1)
