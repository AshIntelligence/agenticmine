# Experiment Analysis Copilot

`Python · experimentation · data`

This computes conversion uplift and a two-proportion significance check, then maps the result to **SHIP / HOLD / STOP**.

Statistical significance is only one input. A rollout also needs guardrails, segment effects, a meaningful effect size and an explanation of what changed in the user journey.

## Run

```bash
python main.py
python main.py --test
```
