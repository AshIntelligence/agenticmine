# Customer Support Knowledge OS

**EVALUATE · Grounded support**

**[▶ Try it live](https://ash-intelligence-lab.streamlit.app/?product=support-knowledge-os)**

### Product question
**Is the available evidence strong enough to answer—or should the product escalate?**

This prototype returns a support answer only when retrieved evidence clears a confidence gate. Otherwise the system produces an escalation state instead of manufacturing certainty.

**Escalation is a valid product outcome.** Deflection only matters when the answer is trustworthy enough that the customer does not have to reopen the issue later.

## What the code models

- a small knowledge base
- query-to-evidence matching
- confidence threshold
- **ANSWER / ESCALATE** behavior
- sources behind the answer

A production version would add article freshness, entitlement context, escalation reason codes and closed-loop feedback from resolved cases.

## Run

```bash
python main.py
python main.py --test
```

Part of the **EVALUATE** pillar in the [Ash Intelligence Lab](../../README.md).
