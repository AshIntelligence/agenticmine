# Telemetry Anomaly → Product Action

`Python · observability`

This detects rolling anomalies and maps the signal to an investigation or product action.

I am less interested in another red chart than in whether telemetry changes rollout, prioritization or diagnosis. The output therefore carries the anomaly into a next-action state instead of stopping at detection.

## Run

```bash
python main.py
python main.py --test
```
