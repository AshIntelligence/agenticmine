# Telemetry Anomaly → Product Action

**EVALUATE · Observability**

**[▶ Try it live](https://ash-intelligence-lab.streamlit.app/?product=telemetry-anomaly-to-action)**

### Product question
**What should a metric anomaly change in the product—not merely on a dashboard?**

This prototype detects rolling anomalies and maps each signal to an investigation or product action.

The useful output is not a red chart. It is the decision the signal changes: **rollout, prioritization, diagnosis or follow-up work.**

## What the code models

- rolling baseline
- anomaly threshold
- anomalous points
- action-oriented output

A fuller version would combine business and system metrics, attach ownership, suppress repeated noise and track whether the recommended action actually improved the underlying signal.

## Run

```bash
python main.py
python main.py --test
```

Part of the **EVALUATE** pillar in the [Ash Intelligence Lab](../../README.md).
