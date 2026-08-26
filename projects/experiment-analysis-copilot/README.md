# Experiment Analysis Copilot

**EVALUATE · Experimentation**

**[▶ Try it live](https://ash-intelligence-lab.streamlit.app/?product=experiment-analysis-copilot)**

This prototype calculates conversion uplift and a two-proportion significance check, then returns **SHIP / HOLD / STOP**.

Statistical significance is one input, not the launch decision. A real rollout still needs effect size, guardrails, segment behavior and an explanation of what changed in the user journey.

## What it reports

- control and treatment conversion rates
- absolute and relative uplift
- significance threshold
- decision state: **SHIP / HOLD / STOP**

The useful metric is the one that changes the product decision.

## Run

```bash
python main.py
python main.py --test
```

Part of the **EVALUATE** pillar in the [Ash Intelligence Lab](../../README.md).
