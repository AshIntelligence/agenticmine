# Evidence-Weighted Product Prioritization

**EVALUATE · Product strategy**

**[▶ Try it live](https://ash-intelligence-lab.streamlit.app/?product=product-prioritization-engine)**

### Product question
**Which product bet deserves capacity when impact is only one part of the decision?**

This prototype ranks product bets using **impact, evidence and leverage** against **effort, dependencies, control burden and opportunity cost**.

The score is a decision aid, not an oracle. Two ideas with similar scores can still deserve different choices if one creates a platform option, carries irreversible risk or blocks another critical path.

## What the code makes visible

- expected impact
- strength of evidence
- platform / reuse leverage
- engineering effort and dependencies
- control burden
- opportunity cost

The point is to make the tradeoff inspectable before a roadmap conversation becomes a contest of confidence.

## Run

```bash
python main.py
python main.py --test
```

Part of the **EVALUATE** pillar in the [Ash Intelligence Lab](../../README.md).
