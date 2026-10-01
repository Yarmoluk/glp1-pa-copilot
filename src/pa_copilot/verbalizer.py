"""Optional wording stage. The rule walk remains the source of truth."""
from __future__ import annotations

import json
import os
import re
from dataclasses import asdict
from typing import Protocol

from .core import Result, render

RULE_WALK_ID = "rule-walk-v1"
STUB_ID = "verbalizer-stub-v1"
LIVE_ID = "verbalizer-live"
CITATION = re.compile(r"\[([A-Za-z0-9_, -]+)\]$")
EDGE_ID = re.compile(r"\bPA-E\d+\b")


class DraftVerbalizer(Protocol):
    renderer_id: str

    def verbalize(self, results: list[Result]) -> str: ...


class RuleWalkRenderer:
    renderer_id = RULE_WALK_ID

    def verbalize(self, results: list[Result]) -> str:
        return render(results)[0]


class StubVerbalizer:
    renderer_id = STUB_ID

    def __init__(self, mode: str = "faithful"):
        if mode not in {"faithful", "hostile"}:
            raise ValueError("stub mode must be faithful or hostile")
        self.mode = mode

    def verbalize(self, results: list[Result]) -> str:
        draft = render(results)[0]
        if self.mode == "hostile":
            return draft + "\nFabricated policy edge was added. [PA-E999]"
        return draft


class LiveVerbalizer:
    renderer_id = LIVE_ID

    def verbalize(self, results: list[Result]) -> str:
        # Imported only when a key exists and VERBALIZER=live. Clone and CI need no SDK.
        from openai import OpenAI

        response = OpenAI().responses.create(
            model=os.environ.get("OPENAI_MODEL", "gpt-6-astra"),
            instructions=(
                "You verbalize only the supplied synthetic rule-walk results. "
                "Return exactly one line per result in the same order, formatted "
                "'<criterion>: <outcome>; <plain-language wording>. [<edge id or MISSING>]'. "
                "Copy each criterion, outcome, and citation exactly. Do not infer a fact, "
                "add an edge, change a missing or contradictory result to met, or take an action. "
                "End with the supplied draft-disposition line exactly. No heading or extra text."
            ),
            input=json.dumps({
                "synthetic": True,
                "rule_walk": [asdict(result) for result in results],
                "draft_disposition_line": render(results)[0].splitlines()[-1],
            }),
        )
        return response.output_text


def select_verbalizer() -> DraftVerbalizer:
    mode = os.environ.get("VERBALIZER", "rule-walk").lower()
    if mode == "rule-walk":
        return RuleWalkRenderer()
    if mode == "stub":
        return StubVerbalizer("faithful")
    if mode == "stub-hostile":
        return StubVerbalizer("hostile")
    if mode == "live":
        return LiveVerbalizer() if os.environ.get("OPENAI_API_KEY") else StubVerbalizer("faithful")
    raise ValueError("VERBALIZER must be rule-walk, stub, stub-hostile, or live")


def citation_errors(draft: str, results: list[Result]) -> list[str]:
    """Reject every invented ID and any changed criterion result or disposition."""
    lines = draft.splitlines()
    expected_disposition = render(results)[0].splitlines()[-1]
    allowed = {edge_id for result in results for edge_id in result.edge_ids}
    errors: list[str] = []
    if len(lines) != len(results) + 1:
        errors.append("draft line count differs from rule walk")
    for index, result in enumerate(results):
        if index >= len(lines):
            break
        line = lines[index].strip()
        if not line.startswith(f"{result.criterion}: {result.outcome};"):
            errors.append(f"{result.criterion} outcome or order changed")
        citation = CITATION.search(line)
        expected_ids = list(result.edge_ids) or ["MISSING"]
        cited = [part.strip() for part in citation.group(1).split(",")] if citation else []
        if cited != expected_ids:
            errors.append(f"{result.criterion} citation differs from returned edge")
        if any(edge_id not in allowed for edge_id in EDGE_ID.findall(line)):
            errors.append(f"{result.criterion} contains an invented edge id")
    if len(lines) > len(results) and lines[len(results)].strip() != expected_disposition:
        errors.append("draft disposition changed")
    for line in lines[len(results) + 1:]:
        if any(edge_id not in allowed for edge_id in EDGE_ID.findall(line)):
            errors.append("extra line contains an invented edge id")
    return errors
