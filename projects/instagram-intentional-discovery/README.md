# Intentional Discovery Study

**DECIDE · Ranking / attention**

**[▶ Try it live](https://ash-intelligence-lab.streamlit.app/?product=instagram-intentional-discovery)**

This independent study uses a synthetic social-discovery surface to test a ranking objective built around **relevance, novelty, creator diversity, content quality and a finite attention budget**.

The ranking deliberately allows **done for now** to be a good outcome. Session length is not treated as the only measure of success.

## What the code models

- stated interests
- novelty and creator repetition
- quality / ragebait penalty
- item duration
- finite session budget

The implementation is a small ranking study, not an attempt to reproduce a production recommender.

## Run

```bash
python main.py
python main.py --test
```

Part of the **DECIDE** pillar in the [Ash Intelligence Lab](../../README.md).
