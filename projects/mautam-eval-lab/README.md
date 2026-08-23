# MAUTAM AI Product Evaluation

![MAUTAM architecture](../../docs/assets/mautam-system.svg)

`Python · AI evaluation · release gates`

MAUTAM is the scorecard I use to connect model behavior to product behavior:

- **M**odel & Response Quality
- **A**doption
- **U**ser Workflow Success
- **T**rust & Controls
- **A**vailability & Health
- **M**easurable Business Impact

I wanted trust and operational health to act as gates, not numbers a strong response-quality score could average away. The implementation combines a weighted product score with explicit hard stops and produces one of four release states: **SHIP / TUNE / SIMPLIFY / STOP**.

## What the code models

The current prototype has two evaluation levels:

1. **Snapshot evaluation** — weighted contributions, weakest-lens detection, configurable release thresholds and explicit trust / availability gate failures.
2. **Window evaluation** — average lens health, per-lens volatility and a simple improving / stable / degrading trend across repeated snapshots.

That keeps a single good run from becoming the whole product story.

## Architecture

```mermaid
flowchart LR
  Q[Model & response quality] --> D{Release decision}
  A[Adoption] --> D
  U[Workflow success] --> D
  T[Trust & controls] --> D
  H[Availability & health] --> D
  I[Measurable impact] --> D
  D --> S[SHIP]
  D --> N[TUNE]
  D --> M[SIMPLIFY]
  D --> X[STOP]
  W[Repeated snapshots] --> V[Trend + volatility]
  V --> D
```

## Decision model

```text
weighted product score
        +
trust / availability hard gates
        +
window trend + volatility
        ↓
SHIP · TUNE · SIMPLIFY · STOP
```

## Run

```bash
python main.py
python main.py --test
```

## Signals

In a fuller implementation I would feed this from grounded-response evals, workflow completion, repeat adoption, human-review outcomes, latency/tool failures, availability and a business outcome such as time-to-value, risk reduced or cost avoided.

## What this catches

A strong demo with weak workflow completion. High usage with poor permissions. Great offline scores with failing tools. Interesting AI that never earns measurable product value. A point-in-time score that looks healthy while the underlying trend is degrading.

## Next

The next version would consume versioned trace windows, add cohort trends and confidence intervals, and make release gates configurable by capability rather than global.
