# Headline

The most important line in my AI demo is the one it refuses to write.

# Post

The most important line in my AI demo is the one it refuses to write.

I built a GLP-1 prior-authorization draft gate to make one boundary visible: a model can put a returned path into words. It cannot add a policy edge.

The workflow starts with a synthetic request. A rule walk checks nine declared policy edges. Missing evidence stays visible. An optional verbalizer receives the results, and every draft line must cite a returned edge or carry MISSING. A human accepts or edits the draft. Submission stays blocked.

Then I gave the verbalizer a hostile mode: append a fabricated edge.

The draft gets rejected. CI checks that rejection.

On the frozen 20-case synthetic test split:
• 0 invalid actions
• 100% abstention on the 3 out-of-graph asks
• 100% citation coverage

Those results describe this small fixture. They do not establish clinical performance or generalization.

The graphic shows the actual nine-edge topology of the hand-written synthetic overlay. The published glp1-obesity CKG and ckg-mcp are not loaded here. Graphify.md's graph-creation process is not included.

This is the engineering question I wanted a reviewer to be able to answer: where does the model's authority end, and what happens when it crosses that boundary?

Explore the graph, clone the repo, and run a complete case and a missing-lab case. No API key needed.

Demo and guide: https://yarmoluk.github.io/glp1-pa-copilot/
Code: https://github.com/Yarmoluk/glp1-pa-copilot

What failure would you add to the test suite before considering a shadow pilot?

#ForwardDeployedEngineering #KnowledgeGraphs #AgenticAI

# Image alt text

A directed graph of the nine declared requires edges in a synthetic GLP-1 prior-authorization fixture. A Wegovy start request connects to scope, starting dose, lifestyle documentation, prior therapy, contraindications, concurrent therapy, eGFR documentation and A1c documentation. The scope node connects to the BMI criterion. An optional verbalizer follows the rule walk, a citation gate rejects fabricated PA-E999, and a human reviews the draft. The graphic labels the data synthetic and reports fixture evaluation results.
