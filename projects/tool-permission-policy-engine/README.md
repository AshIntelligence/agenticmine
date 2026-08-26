# Agent Tool Permission Policy

**CONTROL · Agent safety / platform**

**[▶ Try it live](https://ash-intelligence-lab.streamlit.app/?product=tool-permission-policy-engine)**

### Product question
**Having technical access is not the same as having permission to take this action—so what should the agent be allowed to do?**

This prototype evaluates a tool call against **role, action type, data sensitivity and approval state**.

A refund, publish, transfer or deletion can require different approval and reversibility rules even when the same service identity technically has API access. The policy boundary therefore sits between planning and execution.

## What the code models

- caller role
- requested tool + action
- data sensitivity
- approval state
- explicit **ALLOW / REVIEW / DENY** outcome

A fuller version would version policy, attach each decision to the audit trace and carry a stable request/action ID through approval and execution.

## Run

```bash
python main.py
python main.py --test
```

Part of the **CONTROL** pillar in the [Ash Intelligence Lab](../../README.md).
