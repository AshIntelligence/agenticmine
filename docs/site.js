const P=[
['MAUTAM AI Product Evaluation','AI Evaluation','Quality, adoption, workflow success, trust, health and impact','mautam-eval-lab'],
['Agent vs Workflow Router','Agent Architecture','Deterministic, assisted or autonomous by context','agent-vs-workflow-router'],
['Grounded RAG Quality Gate','RAG / Evals','Evidence coverage, citations and contradiction fallback','rag-quality-gate'],
['Human-in-the-Loop Risk Router','AI Safety','Consequence, confidence and reversibility drive autonomy','human-in-loop-risk-router'],
['Finance Close Orchestrator','Multi-Agent / Fintech','Dependency-bound specialist stages with controller approval','finance-close-orchestrator'],
['Payment Provider Onboarding','Payments Platform','Reusable provider contract with regional launch gates','payment-provider-onboarding'],
['Fraud Signal Decision Engine','Risk Decisioning','Explainable allow, review and block boundaries','fraud-signal-decision-engine'],
['Billing Reconciliation Observatory','Fintech Reliability','End-to-end usage, rating and invoice correctness','billing-reconciliation-observatory'],
['Incident Triage Agent','Reliability','Severity, owner and next action from incident evidence','incident-triage-agent'],
['Voice of Customer Synthesis','Product Discovery','Qualitative sentiment joined with quantitative usage evidence','voc-synthesis-studio'],
['PRFAQ Product Spec Agent','Product Craft','Brief to promise, measures, constraints, risks and open questions','prfaq-product-spec-agent'],
['Evidence-Weighted Prioritization','Product Strategy','Impact and evidence against effort, dependencies and control burden','product-prioritization-engine'],
['Experiment Analysis Copilot','Experimentation','Uplift and significance mapped to a product decision','experiment-analysis-copilot'],
['Telemetry Anomaly → Product Action','Observability','Signals that end in investigation or product action','telemetry-anomaly-to-action'],
['Retrieval Evaluation Benchmark','RAG Evaluation','Precision@K, Recall@K, MRR and nDCG','retrieval-eval-benchmark'],
['Agent Tool Permission Policy','Agent Platform','Role, sensitivity, action, approval and audit','tool-permission-policy-engine'],
['Career Discovery Ranking Study','Product Study','Career fit, growth, freshness and location over raw engagement','linkedin-career-discovery'],
['Intentional Discovery Study','Product Study','Relevance, novelty, diversity and a user-defined time budget','instagram-intentional-discovery'],
['Customer Support Knowledge OS','RAG / Support','Answer with evidence or explicitly escalate','support-knowledge-os'],
['Agentic Product Control Plane','AI Platform','Registry, eval gates, cost budgets and rollout control','agentic-product-control-plane']
];
document.getElementById('grid').innerHTML=P.map(x=>`<article class="card"><div class="cat">${x[1]}</div><h3>${x[0]}</h3><p>${x[2]}</p><a href="https://github.com/AshIntelligence/agenticmine/tree/main/projects/${x[3]}">Code + notes →</a></article>`).join('');
