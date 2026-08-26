# Career Discovery Ranking Study

**DECIDE · Ranking / career discovery**

**[▶ Try it live](https://ash-intelligence-lab.streamlit.app/?product=linkedin-career-discovery)**

### Product question
**Can a career-discovery surface optimize for durable fit and growth rather than treating clicks or session time as the goal?**

This independent product study uses a synthetic opportunity set to rank roles using **skill fit, growth adjacency, freshness and location preference**.

The small ranking model makes the objective inspectable: instead of emitting only a final rank, it exposes the component scores behind the recommendation.

## What the code models

- current skills
- skills the user wants to grow
- location preference
- opportunity freshness
- transparent component scoring

The product principle is that recommendation quality should reflect the user outcome the surface is supposed to create—not merely engagement with the surface itself.

## Run

```bash
python main.py
python main.py --test
```

Part of the **DECIDE** pillar in the [Ash Intelligence Lab](../../README.md).
