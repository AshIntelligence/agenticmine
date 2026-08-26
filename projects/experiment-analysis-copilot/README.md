# Experiment Analysis Copilot

**EVALUATE · Experimentation**

**[▶ Try it live](https://ash-intelligence-lab.streamlit.app/?product=experiment-analysis-copilot)**

### Product question
**Does the experiment evidence justify SHIP, HOLD or STOP?**

This prototype computes conversion uplift and a two-proportion significance check, then turns the result into an explicit product decision.

Statistical significance is deliberately not treated as the whole answer. A real rollout also needs effect size, guardrails, segment behavior and an explanation of what changed in the user journey.

## What the code makes inspectable

- control and treatment conversion rates
- absolute/relative uplift
- significance threshold
- decision state: **SHIP / HOLD / STOP**

The product principle is simple: **measurement should change the roadmap, not merely decorate a launch review.**

## Run

```bash
python main.py
python main.py --test
```

Part of the **EVALUATE** pillar in the [Ash Intelligence Lab](../../README.md).
