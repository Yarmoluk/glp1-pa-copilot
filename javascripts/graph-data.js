// Generated from data/synthetic-policy.json; edit that file, then run scripts/sync_demo_visual.py.
window.PA_GRAPH_DATA = {
  "edges": {
    "PA-E02": {
      "from": "adult_weight_management",
      "id": "PA-E02",
      "rationale": "Public payer BMI pattern, adapted as a fictional criterion; not that payer's determination.",
      "relation": "requires",
      "source": "https://ams-gateway.uhcprovider.com/content/dam/provider/docs/public/prior-auth/uhccp-pharmacy-forms/d-g/NC-GLP-1-Weight-Management-PA-Form.pdf",
      "to": "bmi_30_or_27_with_comorbidity"
    },
    "PA-E08": {
      "from": "wegovy_start",
      "id": "PA-E08",
      "rationale": "Completeness and safety-review prompt only; no eGFR cutoff is encoded.",
      "relation": "requires",
      "source": "https://www.accessdata.fda.gov/drugsatfda_docs/label/2026/215256s030lbl.pdf",
      "to": "renal_value_documented"
    }
  },
  "policy_id": "SYN-REGIONAL-WEGOVY-2026-01",
  "synthetic": true
};
