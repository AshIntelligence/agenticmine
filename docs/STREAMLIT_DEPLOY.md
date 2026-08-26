# Interactive Systems Lab deployment

The public lab is deployed from `streamlit_app.py` at the repository root.

## Current deployment

- Live app: https://ash-intelligence-lab.streamlit.app/
- Repository: `AshIntelligence/agenticmine`
- Branch: `main`
- App file: `streamlit_app.py`
- Python: 3.12

The root `requirements.txt` contains the app dependencies. Streamlit Community Cloud redeploys changes from `main`.

## Deep links

Every system can be opened directly with the `product` query parameter. Examples:

```text
https://ash-intelligence-lab.streamlit.app/?product=mautam-evaluation
https://ash-intelligence-lab.streamlit.app/?product=agentic-product-control-plane
https://ash-intelligence-lab.streamlit.app/?product=fraud-signal-decision-engine
https://ash-intelligence-lab.streamlit.app/?product=support-knowledge-os
```

The home page leads with the three flagship systems, then exposes the full 20-system catalog and grounded document Q&A.

## Verification

Automated CI verifies:

1. the catalog maps exactly 20 unique project engines;
2. both Streamlit entrypoints boot without exceptions;
3. every `?product=<slug>` route renders;
4. the `Run system` form submits for all 20 systems;
5. grounded Q&A returns an answer, evidence and evaluation output;
6. an invalid product route falls back to the lab;
7. behavioral evals and all original project demos/self-checks still pass.

Manual release checks:

- open the public app signed out/incognito;
- check responsive layout on a phone-sized viewport;
- confirm outbound GitHub and portfolio links.

## Secrets

The public lab runs without an API key. If model-backed behavior is enabled later, credentials belong in Streamlit Community Cloud app secrets. A real `.streamlit/secrets.toml` is ignored by Git and must never be committed.
