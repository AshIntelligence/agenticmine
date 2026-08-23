# Payment Provider Onboarding

`Python · fintech platform`

I modeled provider onboarding as a reusable launch contract: required API capabilities, supported markets and currencies, risk thresholds and operational health.

The product question is where to draw the platform boundary. Provider-specific quirks are real, but letting every integration become a one-off makes global payment expansion progressively slower.

## Run

```bash
python main.py
python main.py --test
```

## Design notes

- a common provider contract keeps integrations comparable
- regional requirements stay explicit instead of leaking into the platform core
- launch can fail closed when risk or health gates are not met
- provider variation is represented as configuration, not copied workflow logic
