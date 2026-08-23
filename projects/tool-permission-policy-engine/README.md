# Agent Tool Permission Policy

`Python · agent safety · platform`

This evaluates a tool call against **role, action type, data sensitivity and approval state**.

API scopes are not enough for product-level agent control. A refund, export or deletion can require different approval and reversibility rules even when the same service account technically has access.

## Run

```bash
python main.py
python main.py --test
```

I would put this policy boundary between planning and tool execution, version every policy decision and attach the result to the audit trace.
