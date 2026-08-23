# Incident Triage Agent

`Python · reliability · routing`

This takes noisy incident symptoms and produces **severity, likely owner and next action** before any generated status narrative.

During an incident I want deterministic evidence and routing first. Prose comes after the system has established what it knows, what changed and which team can act.

## Run

```bash
python main.py
python main.py --test
```

A production version would join telemetry, dependency maps, recent deploys and service ownership, then measure routing accuracy and time-to-first-useful-action.
