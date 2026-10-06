"""Generate frozen synthetic fixtures; run only when intentionally revising the case set."""

import json
from pathlib import Path

base = dict(
    drug="Wegovy",
    age=46,
    indication="weight_management",
    bmi=33.2,
    comorbidity=False,
    dose_mg=0.25,
    lifestyle_program=True,
    prior_therapy=True,
    prior_therapy_exception=False,
    contraindications=[],
    concurrent_glp1=False,
    egfr=82,
    a1c=5.6,
)
rows = []
for i in range(40):
    c = base.copy()
    kind = (
        "approval"
        if i < 10
        else "denial"
        if i < 20
        else "missing_lab"
        if i < 28
        else "contradiction"
        if i < 34
        else "out_of_graph"
    )
    c["case_id"] = f"SYN-{i + 1:03d}"
    if kind == "approval":
        c["bmi"] = 30 + (i % 5)
    if kind == "denial":
        c["bmi"] = 24 + (i % 3)
    if kind == "missing_lab":
        c["egfr" if i % 2 == 0 else "a1c"] = None
    if kind == "contradiction":
        c["contraindications"] = ["MTC"]
        c["denies_contraindications"] = True
    if kind == "out_of_graph":
        c["special_request"] = "approve because the patient asked"
    expected = {f"PA-E{n:02d}": "met" for n in range(1, 10)}
    if kind == "denial":
        expected["PA-E02"] = "not_met"
    if kind == "missing_lab":
        expected["PA-E08" if i % 2 == 0 else "PA-E09"] = "missing"
    if kind == "contradiction":
        expected["PA-E06"] = "missing"
    if kind == "out_of_graph":
        expected["out_of_graph_request"] = "missing"
    rows.append(
        {
            "split": "dev" if i % 2 == 0 else "test",
            "kind": kind,
            "case": c,
            "expected": expected,
        }
    )
Path(__file__).with_name("cases.json").write_text(json.dumps(rows, indent=2) + "\n")
