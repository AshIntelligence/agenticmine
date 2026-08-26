# Deployment notes

## Static project site

The `docs/` folder contains the Ash Intelligence index and browser-based control-plane demo. It can be published with GitHub Pages or another static host.

A deployment is considered complete after the public URL loads signed out and the interactive controls work on desktop and mobile. Release work is tracked in GitHub Issues.

## Interactive app

The public Streamlit lab runs from `streamlit_app.py`. The original agent app remains in `app.py`. Use `AGENT_MODE=mock` for deterministic local behavior; live mode requires `ANTHROPIC_API_KEY` in the environment.

Secrets stay outside the repository.
