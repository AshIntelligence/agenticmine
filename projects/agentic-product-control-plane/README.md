# Agentic Product Control Plane

![Agentic Product Control Plane](../../docs/assets/control-plane.svg)

`Python · AI platform · policy controls`

This project puts the main controls around an agent in one place: **registry, tool permissions, approval boundaries, evaluation gates, cost budgets, incident thresholds, rollout state and audit events**.

It keeps three decisions separate:

1. Is the agent registered with the right contract?
2. Is this tool call allowed, denied, or waiting for approval?
3. Do current quality, reliability and cost signals support the next rollout stage?

## What the code models

`AgentSpec` defines registered tools, approval-required tools, rollout stage and quality/cost thresholds.

`authorize_tool(...)` returns **ALLOW / REVIEW / DENY**.

`assess_rollout(...)` checks quality, incident and cost gates separately from tool authorization and returns **HOLD / CANARY / PRODUCTION** with blockers and a next action.

`ControlPlane` keeps an in-memory registry and audit trail so each tool and rollout decision can be traced.

## Architecture

```mermaid
flowchart LR
  R[Agent registry] --> T{Tool policy}
  T --> A[ALLOW]
  T --> H[HUMAN REVIEW]
  T --> D[DENY]

  R --> G{Rollout gate}
  E[Eval score] --> G
  I[Incident rate] --> G
  C[Cost p95] --> G
  G --> X[HOLD]
  G --> Y[CANARY]
  G --> P[PRODUCTION]

  T --> O[Audit events]
  G --> O
```

## Run

```bash
python main.py
python main.py --test
```

The browser prototype lives in [`../../docs/control-plane-demo.html`](../../docs/control-plane-demo.html).

## Next

Add durable execution state, versioned policy, rolling per-agent budgets and a human-approval UI that records reviewer decisions in the audit trail.
