# Retrieval Evaluation Benchmark

**RAG / Evals · runnable synthetic prototype**

Computes **Precision@K, Recall@K, MRR and nDCG** for ranked retrieval experiments.

```bash
python main.py
python main.py --test
```

**Product point:** no single retrieval metric predicts answer usefulness; retrieval changes must ultimately connect to grounded-answer and workflow outcomes.
