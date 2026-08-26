# Retrieval Evaluation Benchmark

**EVALUATE · RAG quality**

**[▶ Try it live](https://ash-intelligence-lab.streamlit.app/?product=retrieval-eval-benchmark)**

### Product question
**Did the retrieval change actually improve evidence quality before generation hides the failure?**

This prototype implements **Precision@K, Recall@K, MRR and nDCG** for ranked retrieval experiments.

The metrics stay separate because they catch different failure modes: top-result quality, relevant-document coverage, first-hit position and ordering quality. None alone proves the final answer is useful, but together they make retrieval changes measurable before the LLM becomes another variable.

## What the code exposes

- Precision@K
- Recall@K
- Mean Reciprocal Rank
- normalized discounted cumulative gain

The product principle: **debug the evidence layer independently before blaming or tuning generation.**

## Run

```bash
python main.py
python main.py --test
```

Part of the **EVALUATE** pillar in the [Ash Intelligence Lab](../../README.md).
