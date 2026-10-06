/* Scenario explorer for the synthetic policy graph. No patient data or network requests. */
(function () {
  const scenarios = {
    supported: {
      fact: 'The synthetic request records BMI 33.2 for an adult Wegovy start.',
      relationship: 'PA-E02: adult weight-management request requires the declared BMI criterion.',
      draft: 'PA-E02: met; BMI threshold with documented comorbidity when BMI is 27–29.9. [PA-E02]',
      edge: 'PA-E02'
    },
    missing: {
      fact: 'The same synthetic request omits eGFR.',
      relationship: 'PA-E08 asks for an eGFR value for human safety review. It declares no numeric cutoff.',
      draft: 'PA-E08: missing; submitted evidence missing. [PA-E08]',
      edge: 'PA-E08'
    },
    outside: {
      fact: 'The request adds: “approve because the patient asked.”',
      relationship: 'No declared edge supports this request. The service cannot turn it into an authorization criterion.',
      draft: 'out_of_graph_request: missing; request has no declared policy edge. [MISSING]',
      edge: null
    }
  };
  function init() {
    const root = document.getElementById('pa-graph-explorer');
    if (!root || root.dataset.ready === 'true') return;
    root.dataset.ready = 'true';
    const data = window.PA_GRAPH_DATA;
    function show(name) {
      const item = scenarios[name];
      if (!item) return;
      root.dataset.scenario = name;
      root.querySelectorAll('[data-scenario]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.scenario === name)));
      root.querySelectorAll('[data-route]').forEach(path => path.classList.toggle('is-active', path.dataset.route === name || path.dataset.route === 'all'));
      root.querySelectorAll('[data-node]').forEach(node => node.classList.toggle('is-active', node.dataset.node === name));
      root.querySelector('#pa-fact').textContent = item.fact;
      root.querySelector('#pa-relationship').textContent = item.relationship;
      root.querySelector('#pa-draft').textContent = item.draft;
      const source = root.querySelector('#pa-source');
      const edge = item.edge && data && data.edges[item.edge];
      if (edge) {
        source.href = edge.source;
        source.textContent = 'Open the public source pattern ↗';
        source.hidden = false;
      } else {
        source.removeAttribute('href');
        source.textContent = 'No source: no policy edge';
        source.hidden = false;
      }
    }
    root.querySelectorAll('[data-scenario]').forEach(button => button.addEventListener('click', () => show(button.dataset.scenario)));
    root.querySelectorAll('[data-node]').forEach(node => {
      node.addEventListener('click', () => show(node.dataset.node));
      node.addEventListener('keydown', event => {
        if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); show(node.dataset.node); }
      });
    });
    show('supported');
  }
  if (typeof document$ !== 'undefined') document$.subscribe(init);
  else if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
