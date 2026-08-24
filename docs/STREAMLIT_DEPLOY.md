# Deploy the Interactive Demo Hub

The deployable entrypoint is `streamlit_app.py` at the repository root.

## Streamlit Community Cloud

Use these deployment values:

- Repository: `AshIntelligence/agenticmine`
- Branch: `main`
- App file: `streamlit_app.py`
- Suggested app URL: `ash-intelligence-lab` (or another available subdomain)
- Python: 3.12

The root `requirements.txt` already contains the Python dependencies used by the app.

After deployment, verify the hub while signed out/incognito before adding the public URL to the README or portfolio.

## Deep links

Each system can be opened directly with the `product` query parameter. For example, once the base URL is known:

```text
https://<app>.streamlit.app/?product=mautam-evaluation
https://<app>.streamlit.app/?product=agentic-product-control-plane
https://<app>.streamlit.app/?product=fraud-signal-decision-engine
https://<app>.streamlit.app/?product=support-knowledge-os
```

The home page exposes all 20 product cards and a grounded Q&A playground.

## Optional model-backed mode

The public hub is deliberately usable without any secret or API key. If a model-backed experience is added later, store credentials in Streamlit Community Cloud app secrets rather than committing a real `.streamlit/secrets.toml` file.

## Release checklist

1. Open the home page signed out and confirm 20 product cards render.
2. Open at least one system in every category.
3. Run the default interaction for all 20 systems.
4. Open the grounded Q&A playground and ask the default question.
5. Confirm the GitHub source links open the matching project folders.
6. Test on both desktop and mobile widths.
7. Only then add the verified public URL to the repository README, standalone flagship READMEs, portfolio, and GitHub profile.
