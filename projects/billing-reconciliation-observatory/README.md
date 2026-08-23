# Billing Reconciliation Observatory

`Python · fintech reliability`

This checks the end-to-end path from **usage → rating → invoice** and turns mismatches into exposure-aware issues.

A local service can look healthy while the final invoice is still wrong, so the checks follow the financial path across handoffs instead of relying on service uptime alone.

## Run

```bash
python main.py
python main.py --test
```

A fuller version would keep a ledger of expected versus observed state, apply tolerance policy by event type and link each mismatch back to the source meter or rating record for investigation.
