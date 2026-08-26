# Intentional Discovery Study

**DECIDE · Ranking / attention**

**[▶ Try it live](https://ash-intelligence-lab.streamlit.app/?product=instagram-intentional-discovery)**

### Product question
**Can a discovery experience treat “done for now” as a successful outcome instead of optimizing every session for maximum time?**

This independent product study uses a synthetic social-discovery surface to explore a ranking objective that balances **relevance, novelty, creator diversity, low-ragebait quality and a user-defined attention budget**.

The point is the objective function and product tradeoff: a ranking system can be technically effective while still optimizing for the wrong user outcome.

## What the code models

- stated interests
- novelty and creator repetition
- quality / ragebait penalty
- item duration
- finite session budget

The result is an inspectable ranking rather than an attempt to recreate any production recommender.

## Run

```bash
python main.py
python main.py --test
```

Part of the **DECIDE** pillar in the [Ash Intelligence Lab](../../README.md).
