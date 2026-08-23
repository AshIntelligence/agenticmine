# Customer Support Knowledge OS

`Python · RAG · support`

This returns a support answer only when evidence clears a confidence gate; otherwise it escalates.

Escalation is a valid product state. Deflection only matters when the answer is trustworthy enough that the customer does not have to reopen the issue later.

## Run

```bash
python main.py
python main.py --test
```

A production version would add article freshness, entitlement context, escalation reason codes and closed-loop feedback from resolved cases.
