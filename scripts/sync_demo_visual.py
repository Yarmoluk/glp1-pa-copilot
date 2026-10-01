"""Copy two hand-specified demo edges into the static illustration.

This is presentation data synchronization, not CKG extraction or creation.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
policy = json.loads((ROOT / "data/synthetic-policy.json").read_text())
lookup = {edge["id"]: edge for edge in policy["edges"]}
ids = ("PA-E02", "PA-E08")
assert policy["synthetic"] is True and all(edge_id in lookup for edge_id in ids)
subset = {edge_id: {key: lookup[edge_id][key] for key in ("id", "from", "to", "relation", "source", "rationale")} for edge_id in ids}
text = "// Generated from data/synthetic-policy.json; edit that file, then run scripts/sync_demo_visual.py.\n"
text += "window.PA_GRAPH_DATA = " + json.dumps({"policy_id": policy["policy_id"], "synthetic": True, "edges": subset}, indent=2, sort_keys=True) + ";\n"
output = ROOT / "docs/javascripts/graph-data.js"
if "--check" in sys.argv:
    if not output.exists() or output.read_text() != text:
        raise SystemExit("Graph explorer data is stale; run python scripts/sync_demo_visual.py")
else:
    output.write_text(text)
