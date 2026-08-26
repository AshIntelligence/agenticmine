# Billing Reconciliation Observatory

**DECIDE · Fintech reliability**

**[▶ Try it live](https://ash-intelligence-lab.streamlit.app/?product=billing-reconciliation-observatory)**

### Product question
**Where did financial truth diverge across usage → rating → invoice, and what should happen next?**

A local service can be technically healthy while the final invoice is still wrong. This prototype follows the financial path across handoffs, compares expected and observed state, and turns a mismatch into an investigation-ready exception.

## What the code models

- usage quantity and rated unit price
- expected versus observed invoice amount
- tolerance policy
- record-level reconciliation output

The important product boundary is the **end-to-end invariant**, not the health of any single component.

## Run

```bash
python main.py
python main.py --test
```

A fuller version would keep authoritative expected/observed state, apply tolerance policy by event type, preserve lineage back to the source meter/rating record, and route ambiguous failures to controlled recovery rather than blind replay.

Part of the **DECIDE** pillar in the [Ash Intelligence Lab](../../README.md).
