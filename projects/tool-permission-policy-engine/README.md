# Agent Tool Permission Policy

**CONTROL · Agent safety / platform**

**[▶ Try it live](https://ash-intelligence-lab.streamlit.app/?product=tool-permission-policy-engine)**

This prototype evaluates a tool call against **role, action type, data sensitivity and approval state**.

Technical API access is not the same as product permission. Refunds, publishes, transfers and deletions can require different approval rules even when the same service identity can reach the API. The policy check therefore sits between planning and execution.

## What the code models

- caller role
- requested tool and action
- data sensitivity
- approval state
- **ALLOW / REVIEW / DENY** outcome

## Next

Version policy, attach each decision to the audit trace and carry a stable request/action ID through approval and execution.

## Run

```bash
python main.py
python main.py --test
```

Part of the **CONTROL** pillar in the [Ash Intelligence Lab](../../README.md).
