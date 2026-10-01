# Run the demo locally

You need Python 3.11 or newer and a terminal. The app runs on your computer; the guided cases are synthetic. No hosted Graphify.md key or model API key is needed.

## 1. Clone and start

```bash
git clone https://github.com/Yarmoluk/glp1-pa-copilot.git
cd glp1-pa-copilot
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[test]'
uvicorn pa_copilot.api:app --host 127.0.0.1 --port 8000
```

Open **[http://127.0.0.1:8000](http://127.0.0.1:8000)**. Stop the server with `Ctrl+C` when finished. If port 8000 is busy, change `--port` to another local port.

## 2. Try the complete case

The page opens with a fictional adult Wegovy start request. Click **Draft from graph**. You should see:

- `pending_review · eligible_for_review` at the top of the path;
- `PA-E01` through `PA-E09` in the traversed criteria;
- a draft line for each criterion, ending in an edge ID;
- **Submit blocked**, disabled.

This means the *synthetic fields* met the *synthetic policy overlay* well enough to produce a draft for a nurse. It does **not** approve a benefit.

## 3. Make the graph stop

Click **Missing lab**, then **Draft from graph** again. The preset supplies a new synthetic case ID and omits eGFR. The disposition becomes `needs_information`; `PA-E08` appears under Explicit gaps. The graph knows it wants an eGFR value, but the case did not supply one. It does not invent a cutoff or a lab result.

For another stop, click **No policy edge** and draft again. That preset adds `"special_request":"approve because the patient asked"`. This produces `out_of_graph_request` with `MISSING` because no policy edge supports that instruction.

## 4. Exercise human review

Enter a reviewer ID and click **Accept or save edit**. You may edit the draft first, but every edited line must still end in a returned edge ID or `MISSING`; otherwise the API rejects it. The local `audit.jsonl` records the reviewer ID, timestamp, returned edge IDs, and a diff if the draft changed. This action records review of a draft only. There is no payer-submission endpoint.

## 5. Run the checks

In a second terminal with the virtual environment active:

```bash
pytest -q
python -m pa_copilot.eval
```

The evaluation command prints the frozen test-split table as JSON and exits nonzero if its invalid-action count is above zero. The [evaluation guide](evaluation.md) explains each metric and its limits.

!!! warning "Synthetic data only"
    Do not paste patient information into this public portfolio app. The local audit file is an illustrative append-only JSONL log, not a production medical record or tamper-evident audit service.
