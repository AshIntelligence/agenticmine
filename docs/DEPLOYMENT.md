# Deployment notes

## Static project site

The `docs/` folder contains the static Ash Intelligence index and the browser-based control-plane prototype. It can be published with GitHub Pages or another static host when a public deployment is needed.

I treat a deployment as complete only after the public URL loads from a signed-out browser and the interactive controls work on desktop and mobile. That work is tracked in GitHub Issues.

## Interactive app

The Streamlit app runs from `app.py` (or `streamlit_app.py` as the Community Cloud entrypoint). Use `AGENT_MODE=mock` for deterministic local behavior; live mode requires `ANTHROPIC_API_KEY` in the environment.

Secrets stay outside the repository.
