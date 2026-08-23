# Agent Tool Permission Policy Engine

**Agent Safety / Platform · runnable synthetic prototype**

Evaluates agent tool calls against role, action type, data sensitivity and approval state.

```bash
python main.py
python main.py --test
```

**Product point:** tool permissions need product semantics, not only API scopes. Consequential actions should be approved, auditable and reversible where possible.
