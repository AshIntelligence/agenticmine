# Product roadmap

I’m focusing the next round of work on a few areas that would make these systems more useful and more realistic.

## Reliability & state

- Persist execution state for multi-step agent workflows
- Keep replayable traces for failed or interrupted runs
- Make side-effecting tasks idempotent where possible

## Evaluation

- Add versioned datasets for MAUTAM and retrieval quality
- Compare model, prompt and policy changes against the same cases
- Track workflow success alongside model-level metrics

## Human control

- Build approval UX for consequential tool calls
- Show reason codes and supporting evidence at review time
- Support rollback where the underlying action can be reversed

## Economics

- Add per-agent and per-workflow cost budgets
- Track token and tool spend
- Define fallback behavior when a workflow is over budget

## Product surface

- Continue the control-plane UI so agent state, eval gates, permissions, budgets and rollout decisions are visible in one place

Current work is tracked in GitHub Issues.