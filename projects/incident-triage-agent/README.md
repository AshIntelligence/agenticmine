# Incident Triage Agent

**DECIDE · Reliability**

**[▶ Try it live](https://ash-intelligence-lab.streamlit.app/?product=incident-triage-agent)**

This prototype takes an incident description plus operational signals and returns **severity, likely owner, matched evidence and next action**.

Routing comes before narrative. The system first establishes impact and ownership; status prose is secondary.

## What the code models

- symptom text
- error rate and affected traffic
- revenue-path criticality
- severity, owner and next-action routing

## Next

Join telemetry, dependency maps, recent deploys and service ownership, then measure routing accuracy and time to first useful action.

## Run

```bash
python main.py
python main.py --test
```

Part of the **DECIDE** pillar in the [Ash Intelligence Lab](../../README.md).
