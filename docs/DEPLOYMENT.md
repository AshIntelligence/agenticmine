# Deployment notes

## GitHub Pages

The `docs/` folder is the static Ash Intelligence index. `.github/workflows/pages.yml` publishes it from `main` whenever the site files change.

## Interactive app

The Streamlit app runs from `app.py` (or `streamlit_app.py` as the Community Cloud entrypoint). Use `AGENT_MODE=mock` for deterministic local behavior; live mode requires `ANTHROPIC_API_KEY` in the environment.

Secrets stay outside the repository.
