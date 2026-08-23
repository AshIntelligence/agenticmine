# Retrieval Evaluation Benchmark

`Python · RAG evaluation`

This implements **Precision@K, Recall@K, MRR and nDCG** for ranked retrieval experiments.

I keep the metrics separate because they catch different failures: top-result quality, relevant-document coverage, first-hit position and ordering quality. None of them alone proves the final answer is useful, but they make retrieval changes measurable before generation muddies the diagnosis.

## Run

```bash
python main.py
python main.py --test
```
