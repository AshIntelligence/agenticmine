# Customer Support Knowledge OS

**RAG / Support · runnable synthetic prototype**

Retrieves a support answer only when evidence clears a confidence gate; otherwise it explicitly escalates.

```bash
python main.py
python main.py --test
```

**Product point:** deflection is only useful when answer quality is high. **ESCALATE** is a healthy product state, not a failure.
