# Publish the portfolio

Target repository: **https://github.com/AshIntelligence/agenticmine**

## Static portfolio site with GitHub Pages

The `docs/` folder contains a self-contained static portfolio and `.github/workflows/pages.yml` deploys it.

1. Open **Settings → Pages**.
2. Set **Source** to **GitHub Actions** once.
3. Push to `main`.

Expected URL: **https://ashintelligence.github.io/agenticmine/**

## Deploy the real Streamlit app

The repository contains `streamlit_app.py`, `requirements.txt`, and `.streamlit/config.toml`.

1. Sign in to Streamlit Community Cloud with GitHub.
2. Choose **Create app**.
3. Repository: **AshIntelligence/agenticmine**.
4. Branch: `main`.
5. App file: `streamlit_app.py`.
6. Deploy.

Keep the public deployment in default mock mode. For a private live-Claude version, store `ANTHROPIC_API_KEY` in Streamlit Secrets, never in the repository.
