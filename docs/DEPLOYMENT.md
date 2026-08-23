# Deployment notes

## Static site

The `docs/` folder contains the static Ash Intelligence index and the browser-based control-plane prototype. `.github/workflows/pages.yml` is configured to deploy that folder from `main` after GitHub Pages is enabled for the repository.

Public hosting is treated as complete only after the deployed URL is verified from a signed-out browser. That activation/verification work is tracked in GitHub Issues.

## Interactive app

The Streamlit app runs from `app.py` (or `streamlit_app.py` as the Community Cloud entrypoint). Use `AGENT_MODE=mock` for deterministic local behavior; live mode requires `ANTHROPIC_API_KEY` in the environment.

Secrets stay outside the repository.
