# Payment Provider Onboarding

**DECIDE · Fintech platform**

**[▶ Try it live](https://ash-intelligence-lab.streamlit.app/?product=payment-provider-onboarding)**

This prototype models provider onboarding as a reusable launch contract: API capabilities, supported markets and currencies, risk thresholds and operational health.

The design split is between the **shared provider contract** and provider- or market-specific configuration. Regional variation stays explicit without copying the entire integration workflow for every provider.

## What the code models

- required provider capabilities
- country and currency fit
- chargeback threshold
- availability threshold
- ready / not-ready launch status

## Design choices

- keep the shared contract stable
- represent regional variation as configuration
- include risk and reliability in launch readiness
- fail closed when a required capability or control is missing

## Run

```bash
python main.py
python main.py --test
```

Part of the **DECIDE** pillar in the [Ash Intelligence Lab](../../README.md).
