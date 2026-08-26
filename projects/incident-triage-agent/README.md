# Incident Triage Agent

**DECIDE · Reliability**

**[▶ Try it live](https://ash-intelligence-lab.streamlit.app/?product=incident-triage-agent)**

### Product question
**Given noisy symptoms, what is the severity, who owns the next move, and what action matters first?**

This prototype turns an incident description plus operational signals into **severity, likely owner, matched evidence and next action** before generating any status narrative.

During an incident, routing and evidence need to be established first. The prose comes after the system has identified what changed, what is known and which team is most likely to act.

## What the code models

- symptom text
- error rate and affected traffic
- revenue-path criticality
- severity / owner / next-action routing

A fuller version would join telemetry, dependency maps, recent deploys and service ownership, then measure routing accuracy and time-to-first-useful-action.

## Run

```bash
python main.py
python main.py --test
```

Part of the **DECIDE** pillar in the [Ash Intelligence Lab](../../README.md).
