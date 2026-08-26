# Customer Support Knowledge OS

**EVALUATE · Grounded support**

**[▶ Try it live](https://ash-intelligence-lab.streamlit.app/?product=support-knowledge-os)**

This prototype answers a support question only when the available evidence clears a confidence gate. Otherwise it returns **ESCALATE**.

Escalation is a normal product state. Deflection only helps when the answer is reliable enough that the customer does not have to reopen the issue later.

## What the code models

- a small knowledge base
- query-to-evidence matching
- confidence threshold
- **ANSWER / ESCALATE** behavior
- source IDs behind the answer

## Next

Add article freshness, entitlement context, escalation reason codes and closed-loop feedback from resolved cases.

## Run

```bash
python main.py
python main.py --test
```

Part of the **EVALUATE** pillar in the [Ash Intelligence Lab](../../README.md).
