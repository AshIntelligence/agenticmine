# Retrieval Evaluation Benchmark

**EVALUATE · RAG quality**

**[▶ Try it live](https://ash-intelligence-lab.streamlit.app/?product=retrieval-eval-benchmark)**

This prototype implements **Precision@K, Recall@K, MRR and nDCG** for ranked retrieval experiments.

The metrics stay separate because they answer different questions: are the top results good, did we retrieve enough of the relevant set, how early did the first useful result appear, and is the ranking ordered well?

## What the code exposes

- Precision@K
- Recall@K
- Mean Reciprocal Rank
- normalized discounted cumulative gain

Retrieval is measured independently so generation does not hide an evidence-layer problem.

## Run

```bash
python main.py
python main.py --test
```

Part of the **EVALUATE** pillar in the [Ash Intelligence Lab](../../README.md).
