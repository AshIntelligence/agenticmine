# Grounded RAG Quality Gate

**RAG / Evaluation · runnable synthetic prototype**

Scores evidence coverage, citation validity and contradictions before an answer can ship.

```bash
python main.py
python main.py --test
```

**Product point:** low grounding confidence should produce an explicit **REVIEW / fallback** state instead of a more confident hallucination.
