# Career Discovery Ranking Study

**DECIDE · Ranking / career discovery**

**[▶ Try it live](https://ash-intelligence-lab.streamlit.app/?product=linkedin-career-discovery)**

This independent study ranks a synthetic opportunity set using **skill fit, growth adjacency, freshness and location preference**.

The model exposes the component scores behind each recommendation instead of returning only a final rank. That makes the ranking objective easy to inspect and tune.

## What the code models

- current skills
- skills the user wants to grow
- location preference
- opportunity freshness
- component scoring

The ranking is optimized for fit and growth, not clicks or session time.

## Run

```bash
python main.py
python main.py --test
```

Part of the **DECIDE** pillar in the [Ash Intelligence Lab](../../README.md).
