# Product roadmap

The lab evolves through a small set of product bets rather than by adding disconnected examples.

## Reliability & state

- Persistent execution state and recovery for multi-step agent workflows
- Replayable traces for failed or interrupted runs
- Idempotent task execution where side effects are possible

## Evaluation

- Versioned evaluation datasets for MAUTAM and retrieval quality
- Regression reports across model / prompt / policy changes
- Workflow-level success metrics in addition to model-level metrics

## Human control

- Approval UX for consequential tool calls
- Clear reason codes and evidence at review time
- Reversible action patterns where the underlying tool permits rollback

## Economics

- Per-agent and per-workflow cost budgets
- Token/tool spend telemetry
- Rollout policies that can degrade gracefully when budgets are exceeded

## Live product surface

- Interactive control-plane demo showing agent state, eval gates, permissions, budgets and rollout decisions in one UI

The active GitHub Issues are the working backlog for these bets.