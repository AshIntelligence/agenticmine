# Billing Reconciliation Observatory

**DECIDE · Fintech reliability**

**[▶ Try it live](https://ash-intelligence-lab.streamlit.app/?product=billing-reconciliation-observatory)**

This prototype follows the financial path from **usage → rating → invoice** and flags where expected and observed state diverge.

A service can be technically healthy while the customer invoice is still wrong, so the check is end-to-end rather than component-by-component.

## What the code models

- usage quantity and rated unit price
- expected versus observed invoice amount
- tolerance policy
- record-level reconciliation output

The core invariant is simple: the financial state at the end of the chain has to reconcile with the state that produced it.

## Run

```bash
python main.py
python main.py --test
```

## Next

Add authoritative expected/observed state, event-specific tolerance policy, lineage back to the source meter or rating record, and controlled recovery for ambiguous failures.

Part of the **DECIDE** pillar in the [Ash Intelligence Lab](../../README.md).
