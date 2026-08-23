# Incident Triage Agent

`Python · reliability · routing`

This takes noisy incident symptoms and produces **severity, likely owner and next action** before generating any status narrative.

During an incident, routing and evidence need to be established first. The prose comes after the system has identified what changed, what is known and which team is most likely to act.

## Run

```bash
python main.py
python main.py --test
```

A fuller version would join telemetry, dependency maps, recent deploys and service ownership, then track routing accuracy and time-to-first-useful-action.
