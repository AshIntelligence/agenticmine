# Agentic Product Control Plane

![Agentic Product Control Plane](../../docs/assets/control-plane.svg)

`Python · AI platform`

This models the control surface I expect around production agents: **registry, tools, eval gates, cost budgets, incident thresholds and rollout state**.

The interesting part is not the agent prompt. It is whether the platform can decide when an agent is allowed to move from **shadow → canary → production**, and why it is being held back.

## Architecture

```mermaid
flowchart LR
  A[Agent spec] --> G{Rollout gate}
  E[Eval score] --> G
  I[Incident rate] --> G
  C[Cost p95] --> G
  G --> H[HOLD]
  G --> Y[CANARY]
  G --> P[PRODUCTION]
```

## Run

```bash
python main.py
python main.py --test
```

The current implementation is deliberately compact, but the boundary is the important part: agent registration and allowed tools are separate from runtime health and promotion policy.
