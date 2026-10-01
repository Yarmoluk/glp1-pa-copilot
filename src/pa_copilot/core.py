"""Illustrative consumer-side traversal over a synthetic policy fixture.

This module does not discover, extract, compress, or generate a CKG.
"""
from __future__ import annotations
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
REQUIRED = tuple(f"PA-E{i:02d}" for i in range(1, 10))
FIELDS = ("indication", "bmi", "comorbidity", "dose_mg", "lifestyle_program", "prior_therapy", "prior_therapy_exception", "contraindications", "concurrent_glp1", "egfr", "a1c", "age")

@dataclass(frozen=True)
class Result:
    criterion: str
    outcome: str  # met | not_met | missing
    edge_ids: tuple[str, ...]
    detail: str

class Graph:
    def __init__(self, policy_path: Path | None = None):
        policy = json.loads((policy_path or ROOT / "data/synthetic-policy.json").read_text())
        if policy.get("synthetic") is not True:
            raise ValueError("Only explicitly synthetic policy is permitted")
        self.policy_id = policy["policy_id"]
        self.edges = {e["id"]: e for e in policy["edges"]}
        if len(self.edges) != len(policy["edges"]):
            raise ValueError("Duplicate edge ID")

    def traverse(self, start: str = "wegovy_start") -> list[dict[str, Any]]:
        """Stable BFS over declared outgoing edges, with no inferred hops."""
        queue, seen, found = [start], {start}, []
        while queue:
            node = queue.pop(0)
            for edge in sorted(self.edges.values(), key=lambda e: e["id"]):
                if edge["from"] != node:
                    continue
                found.append(edge)
                if edge["to"] not in seen:
                    seen.add(edge["to"])
                    queue.append(edge["to"])
        return found

    def validate(self) -> list[str]:
        errors = []
        for edge in self.edges.values():
            if not edge.get("source", "").startswith("https://") or edge.get("relation") != "requires":
                errors.append(f"invalid edge {edge['id']}")
        return errors

def _missing(value: Any) -> bool:
    return value is None or value == "" or value == []

def evaluate(case: dict[str, Any], graph: Graph) -> tuple[list[Result], list[str]]:
    """Evaluate only named, traversed edges. Unknown or absent edges abstain."""
    reached = {e["id"] for e in graph.traverse()}
    results: list[Result] = []
    calls = ["validate_demo_policy", "traverse:wegovy_start"]
    funcs = {
        "PA-E01": lambda c: (c.get("age", 0) >= 18 and c.get("drug") == "Wegovy" and c.get("indication") == "weight_management", "adult Wegovy injection weight-management scope"),
        "PA-E02": lambda c: (c.get("bmi", 0) >= 30 or (c.get("bmi", 0) >= 27 and c.get("comorbidity") is True), "BMI threshold with documented comorbidity when BMI is 27–29.9"),
        "PA-E03": lambda c: (c.get("dose_mg") == 0.25, "0.25 mg weekly injection start dose"),
        "PA-E04": lambda c: (c.get("lifestyle_program") is True, "lifestyle program documented"),
        "PA-E05": lambda c: (c.get("prior_therapy") is True or c.get("prior_therapy_exception") is True, "prior therapy or documented exception"),
        "PA-E06": lambda c: (not bool(c.get("contraindications")), "no submitted label contraindication"),
        "PA-E07": lambda c: (c.get("concurrent_glp1") is False, "no concurrent GLP-1 therapy"),
        "PA-E08": lambda c: (isinstance(c.get("egfr"), (int, float)) and c["egfr"] > 0, "eGFR recorded for human safety review; no cutoff applied"),
        "PA-E09": lambda c: (isinstance(c.get("a1c"), (int, float)) and c["a1c"] > 0, "A1c recorded; no eligibility cutoff applied"),
    }
    inputs = {
        "PA-E01": ("age", "drug", "indication"), "PA-E02": ("bmi",), "PA-E03": ("dose_mg",),
        "PA-E04": ("lifestyle_program",), "PA-E05": ("prior_therapy", "prior_therapy_exception"),
        "PA-E06": ("contraindications",), "PA-E07": ("concurrent_glp1",),
        "PA-E08": ("egfr",), "PA-E09": ("a1c",),
    }
    for edge_id in REQUIRED:
        if edge_id not in reached or edge_id not in graph.edges:
            results.append(Result(edge_id, "missing", (), "criterion edge absent from graph"))
            continue
        fields = inputs[edge_id]
        if any(_missing(case.get(f)) for f in fields if f != "contraindications") or ("contraindications" in fields and case.get("contraindications") is None):
            # For prior therapy, either explicit true or two explicit false values are required.
            results.append(Result(edge_id, "missing", (edge_id,), "submitted evidence missing"))
            continue
        if edge_id == "PA-E02" and 27 <= case["bmi"] < 30 and case.get("comorbidity") is None:
            results.append(Result(edge_id, "missing", (edge_id,), "comorbidity evidence missing"))
            continue
        if edge_id == "PA-E06" and case.get("denies_contraindications") is True and case.get("contraindications"):
            results.append(Result(edge_id, "missing", (edge_id,), "contradictory contraindication statements"))
            continue
        try:
            passed, detail = funcs[edge_id](case)
        except (TypeError, ValueError):
            results.append(Result(edge_id, "missing", (edge_id,), "invalid submitted field"))
            continue
        results.append(Result(edge_id, "met" if passed else "not_met", (edge_id,), detail))
    if case.get("special_request"):
        results.append(Result("out_of_graph_request", "missing", (), "request has no declared policy edge"))
    return results, calls

def render(results: list[Result]) -> tuple[str, str, list[str]]:
    gaps = [r.criterion for r in results if r.outcome == "missing"]
    failed = [r.criterion for r in results if r.outcome == "not_met"]
    disposition = "needs_information" if gaps else ("criteria_not_met" if failed else "eligible_for_review")
    lines = []
    for r in results:
        citation = ",".join(r.edge_ids) if r.edge_ids else "MISSING"
        lines.append(f"{r.criterion}: {r.outcome}; {r.detail}. [{citation}]")
    lines.append(f"Draft disposition: {disposition}; human review required. [{'MISSING' if gaps else ','.join(e for r in results for e in r.edge_ids)}]")
    return "\n".join(lines), disposition, gaps
