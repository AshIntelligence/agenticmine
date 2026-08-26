# Payment Provider Onboarding

**DECIDE · Fintech platform**

**[▶ Try it live](https://ash-intelligence-lab.streamlit.app/?product=payment-provider-onboarding)**

### Product question
**Can this provider launch in this market without turning every integration into a bespoke project?**

This prototype models provider onboarding as a reusable launch contract: API capabilities, supported markets and currencies, risk thresholds and operational health.

The main design choice is what belongs in the **common platform contract** versus provider- or market-specific configuration. Some variation is real; copying the whole workflow for every provider is not.

## What the code models

- required provider capabilities
- country / currency fit
- chargeback threshold
- availability threshold
- explicit ready / not-ready launch output

## Product principles

- keep the shared contract stable
- represent real regional variation as configuration
- make risk and health part of launch readiness
- fail closed when a consequential requirement is missing

## Run

```bash
python main.py
python main.py --test
```

Part of the **DECIDE** pillar in the [Ash Intelligence Lab](../../README.md).
