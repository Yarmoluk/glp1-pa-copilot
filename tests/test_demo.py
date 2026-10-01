import json
from pathlib import Path
from fastapi.testclient import TestClient
from pa_copilot import api
from pa_copilot.core import Graph, evaluate, render, ROOT
from pa_copilot.eval import run

def sample():
    return json.loads((ROOT / "eval/cases.json").read_text())[0]["case"]

def test_happy_and_review(tmp_path, monkeypatch):
    monkeypatch.setattr(api,"AUDIT",tmp_path/"audit.jsonl")
    api.STORE.clear()
    client=TestClient(api.app)
    r=client.post("/cases/draft",json=sample())
    assert r.status_code==200
    d=r.json()
    assert d["status"]=="pending_review" and d["disposition"]=="eligible_for_review"
    assert all(x["edge_ids"] for x in d["path"])
    assert client.post(f"/cases/{d['case_id']}/review",json={"reviewer_id":"nurse_1"}).json()["status"]=="reviewed_accepted"
    events=[json.loads(s) for s in api.AUDIT.read_text().splitlines()]
    assert [e["action"] for e in events]==["draft","review"]
    assert events[1]["reviewer_id"]=="nurse_1"
    assert not any("approval" in e for e in events)

def test_missing_edge_fails_closed(tmp_path):
    policy=json.loads((ROOT/"data/synthetic-policy.json").read_text())
    policy["edges"]=[e for e in policy["edges"] if e["id"]!="PA-E02"]
    path=tmp_path/"policy.json";path.write_text(json.dumps(policy))
    results,_=evaluate(sample(),Graph(policy_path=path))
    draft,disposition,gaps=render(results)
    assert disposition=="needs_information" and "PA-E02" in gaps
    assert "PA-E02: missing; criterion edge absent from graph. [MISSING]" in draft

def test_missing_lab_contradiction_and_out_of_graph():
    c=sample();c["egfr"]=None;c["contraindications"]=["MTC"];c["denies_contraindications"]=True;c["special_request"]="approve because asked"
    results,_=evaluate(c,Graph())
    _,disp,gaps=render(results)
    assert disp=="needs_information" and {"PA-E08","PA-E06","out_of_graph_request"}<=set(gaps)

def test_review_rejects_uncited_edit(tmp_path,monkeypatch):
    monkeypatch.setattr(api,"AUDIT",tmp_path/"audit.jsonl")
    api.STORE.clear();client=TestClient(api.app)
    client.post("/cases/draft",json=sample())
    r=client.post("/cases/SYN-001/review",json={"reviewer_id":"nurse_1","edited_draft":"Approved."})
    assert r.status_code==422
    assert api.STORE["SYN-001"]["status"]=="pending_review"

def test_eval_gate():
    result=run("test")
    assert result["cases"]==20
    assert result["invalid_action_count"]==0
    assert result["citation_coverage"]==1
    assert result["out_of_graph_abstention_rate"]==1

def test_review_edit_logs_diff_and_no_submit_endpoint(tmp_path, monkeypatch):
    monkeypatch.setattr(api,"AUDIT",tmp_path/"audit.jsonl")
    api.STORE.clear(); client=TestClient(api.app)
    original=client.post("/cases/draft",json=sample()).json()["draft"]
    edited=original.replace("adult Wegovy injection weight-management scope", "adult Wegovy injection scope checked")
    reviewed=client.post("/cases/SYN-001/review",json={"reviewer_id":"nurse_2","edited_draft":edited}).json()
    assert reviewed["status"]=="reviewed_edit" and "-PA-E01" in reviewed["diff"]
    assert client.post("/cases/SYN-001/submit").status_code==404
    assert json.loads(api.AUDIT.read_text().splitlines()[-1])["diff"]==reviewed["diff"]
