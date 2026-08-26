const P=[
['MAUTAM AI Product Evaluation','EVALUATE','Quality, adoption, workflow success, trust, availability and impact','mautam-evaluation'],
['Agent vs Workflow Router','CONTROL','Deterministic workflow, assisted agent or autonomous agent based on task context','agent-vs-workflow-router'],
['Grounded RAG Quality Gate','EVALUATE','Grounding, citations and contradiction checks before release','rag-quality-gate'],
['Human-in-the-Loop Risk Router','CONTROL','Consequence, confidence and reversibility set the review boundary','human-in-loop-risk-router'],
['Finance Close Orchestrator','CONTROL','Dependency-bound finance stages with exception handling and controller approval','finance-close-orchestrator'],
['Payment Provider Onboarding','DECIDE','Provider capability, market, risk and reliability checks before launch','payment-provider-onboarding'],
['Fraud Signal Decision Engine','DECIDE','Explainable ALLOW, REVIEW and BLOCK decisions from risk signals','fraud-signal-decision-engine'],
['Billing Reconciliation Observatory','DECIDE','Usage, rating and invoice reconciliation with financial deltas','billing-reconciliation-observatory'],
['Incident Triage Agent','DECIDE','Severity, owner and next action from incident symptoms and impact','incident-triage-agent'],
['Voice of Customer Synthesis','EVALUATE','Customer feedback combined with usage signals before prioritization','voc-synthesis-studio'],
['PRFAQ Product Spec Agent','EVALUATE','Customer promise, measures, constraints, risks and open questions from an early brief','prfaq-product-spec-agent'],
['Evidence-Weighted Prioritization','EVALUATE','Impact, evidence and leverage weighed against effort, dependencies and control cost','product-prioritization-engine'],
['Experiment Analysis Copilot','EVALUATE','Conversion uplift and statistical evidence mapped to SHIP, HOLD or STOP','experiment-analysis-copilot'],
['Telemetry Anomaly → Product Action','EVALUATE','Metric anomalies mapped to investigation or product follow-up','telemetry-anomaly-to-action'],
['Retrieval Evaluation Benchmark','EVALUATE','Precision@K, Recall@K, MRR and nDCG','retrieval-eval-benchmark'],
['Agent Tool Permission Policy','CONTROL','Role, action, sensitivity and approval policy for tool calls','tool-permission-policy-engine'],
['Career Discovery Ranking Study','DECIDE','Skill fit, growth, freshness and location ranking over a synthetic opportunity set','linkedin-career-discovery'],
['Intentional Discovery Study','DECIDE','Relevance, novelty, diversity, quality and a finite attention budget','instagram-intentional-discovery'],
['Customer Support Knowledge OS','EVALUATE','Answer from evidence when confidence clears the gate; otherwise escalate','support-knowledge-os'],
['Agentic Product Control Plane','CONTROL','Registry, permissions, eval gates, cost budgets and rollout control','agentic-product-control-plane']
];
document.getElementById('grid').innerHTML=P.map(x=>`<article class="card"><div class="cat">${x[1]}</div><h3>${x[0]}</h3><p>${x[2]}</p><a href="https://github.com/AshIntelligence/agenticmine/tree/main/projects/${x[3]}">Code + notes →</a></article>`).join('');
