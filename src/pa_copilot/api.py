"""Local-only demo API. Never call an external payer endpoint."""

from __future__ import annotations
import difflib
import json
import os
import re
import threading
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from .core import Graph, evaluate, render, ROOT
from .verbalizer import citation_errors, select_verbalizer

app = FastAPI(title="Synthetic GLP-1 prior-authorization draft gate")
GRAPH = Graph()
AUDIT = Path(os.environ.get("AUDIT_PATH", str(ROOT / "audit.jsonl")))
STORE: dict[str, dict] = {}
LOCK = threading.Lock()


class CaseRequest(BaseModel):
    case_id: str = Field(min_length=1, max_length=80, pattern=r"^[A-Za-z0-9_-]+$")
    drug: str | None = None
    age: int | None = None
    indication: str | None = None
    bmi: float | None = None
    comorbidity: bool | None = None
    dose_mg: float | None = None
    lifestyle_program: bool | None = None
    prior_therapy: bool | None = None
    prior_therapy_exception: bool | None = None
    contraindications: list[str] | None = None
    denies_contraindications: bool | None = None
    concurrent_glp1: bool | None = None
    egfr: float | None = None
    a1c: float | None = None
    special_request: str | None = None


class ReviewRequest(BaseModel):
    reviewer_id: str = Field(min_length=1, max_length=80, pattern=r"^[A-Za-z0-9_-]+$")
    edited_draft: str | None = None


def audit(event: dict) -> None:
    event = {
        "event_id": str(uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **event,
    }
    AUDIT.parent.mkdir(parents=True, exist_ok=True)
    with LOCK:
        fd = os.open(AUDIT, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
        try:
            os.write(fd, (json.dumps(event, sort_keys=True) + "\n").encode())
            os.fsync(fd)
        finally:
            os.close(fd)


def valid_citations(draft: str, allowed: set[str]) -> bool:
    for sentence in draft.splitlines():
        if not sentence.strip():
            continue
        match = re.search(r"\[([A-Za-z0-9_, -]+)\]$", sentence.strip())
        if not match:
            return False
        cites = {x.strip() for x in match.group(1).split(",")}
        if not cites or not cites <= allowed | {"MISSING"}:
            return False
        if any(
            edge_id not in allowed for edge_id in re.findall(r"\bPA-E\d+\b", sentence)
        ):
            return False
    return True


@app.get("/")
def home():
    return FileResponse(ROOT / "static/index.html")


@app.get("/health")
def health():
    return {
        "ok": not GRAPH.validate(),
        "graph_errors": GRAPH.validate(),
        "policy_id": GRAPH.policy_id,
    }


@app.post("/cases/draft")
def draft_case(case: CaseRequest):
    errors = GRAPH.validate()
    if errors:
        raise HTTPException(503, {"graph_errors": errors})
    payload = case.model_dump()
    results, calls = evaluate(payload, GRAPH)
    _, disposition, gaps = render(results)
    edge_ids = sorted({eid for r in results for eid in r.edge_ids})
    try:
        verbalizer = select_verbalizer()
        draft = verbalizer.verbalize(results)
    except Exception as exc:
        raise HTTPException(
            503, f"verbalizer unavailable: {type(exc).__name__}"
        ) from exc
    errors = citation_errors(draft, results)
    if errors:
        audit(
            {
                "action": "draft_rejected",
                "case_id": case.case_id,
                "tool_calls": calls,
                "edge_ids": edge_ids,
                "renderer_id": verbalizer.renderer_id,
                "reviewer_id": None,
                "status": "blocked_invalid_citation",
                "validation_errors": errors,
            }
        )
        raise HTTPException(422, {"validation_errors": errors})
    record = {
        "case_id": case.case_id,
        "policy_id": GRAPH.policy_id,
        "status": "pending_review",
        "disposition": disposition,
        "draft": draft,
        "gaps": gaps,
        "path": [
            {
                **r.__dict__,
                "source": GRAPH.edges.get(r.criterion, {}).get("source"),
                "relation": GRAPH.edges.get(r.criterion, {}).get("relation"),
            }
            for r in results
        ],
        "edge_ids": edge_ids,
        "tool_calls": calls,
        "renderer_id": verbalizer.renderer_id,
    }
    with LOCK:
        if case.case_id in STORE:
            raise HTTPException(409, "case id already exists in this process")
        STORE[case.case_id] = record
    audit(
        {
            "action": "draft",
            "case_id": case.case_id,
            "tool_calls": calls,
            "edge_ids": edge_ids,
            "renderer_id": verbalizer.renderer_id,
            "reviewer_id": None,
            "status": "pending_review",
        }
    )
    return record


@app.get("/cases/{case_id}")
def get_case(case_id: str):
    if case_id not in STORE:
        raise HTTPException(404, "case not found")
    return STORE[case_id]


@app.post("/cases/{case_id}/review")
def review(case_id: str, request: ReviewRequest):
    with LOCK:
        record = STORE.get(case_id)
        if record is None:
            raise HTTPException(404, "case not found")
        if record["status"] != "pending_review":
            raise HTTPException(409, "already reviewed")
        previous = record["draft"]
        edited = request.edited_draft if request.edited_draft is not None else previous
        if not valid_citations(edited, set(record["edge_ids"])):
            raise HTTPException(
                422, "each draft line must end in a returned edge id or MISSING"
            )
        diff = "\n".join(
            difflib.unified_diff(
                previous.splitlines(),
                edited.splitlines(),
                fromfile="draft",
                tofile="reviewed",
                lineterm="",
            )
        )
        record["draft"] = edited
        record["status"] = "reviewed_edit" if diff else "reviewed_accepted"
        record["reviewer_id"] = request.reviewer_id
        record["reviewed_at"] = datetime.now(timezone.utc).isoformat()
        record["diff"] = diff
    audit(
        {
            "action": "review",
            "case_id": case_id,
            "tool_calls": [],
            "edge_ids": record["edge_ids"],
            "renderer_id": record["renderer_id"],
            "reviewer_id": request.reviewer_id,
            "status": record["status"],
            "diff": diff,
        }
    )
    return record
