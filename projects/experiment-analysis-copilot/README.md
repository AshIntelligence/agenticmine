# Experiment Analysis Copilot

`Python · experimentation · data`

This computes conversion uplift and a two-proportion significance check, then maps the result to **SHIP / HOLD / STOP**.

Statistical significance is one input. A real rollout still needs guardrails, segment effects, a product-sized effect and an understanding of what changed in the user journey.

## Run

```bash
python main.py
python main.py --test
```
