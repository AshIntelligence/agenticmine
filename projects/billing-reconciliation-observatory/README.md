# Billing Reconciliation Observatory

`Python · fintech reliability`

This checks the end-to-end path from **usage → rating → invoice** and turns mismatches into exposure-aware issues.

I built the checks at the financial-path level because every local service can report healthy while the customer invoice is still wrong. Correctness has to be reconciled across the handoffs, not inferred from service uptime.

## Run

```bash
python main.py
python main.py --test
```

The natural production extension is a ledger of expected vs. observed state, tolerance policy by event type and automated investigation links back to the source meter/rating record.
