# Running Ash Intelligence locally

## Interactive 20-product Demo Hub

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

This is the main product-facing experience. It exposes all 20 systems as interactive cards and includes a grounded document-agent Q&A playground. The 20 product forms call the original engines under `projects/`.

## Original agent app

```bash
AGENT_MODE=mock streamlit run app.py
```

The default mock mode is deterministic and does not need an API key.

## Run the project checks

```bash
python tools/run_systems.py
```

## Tests and evals

```bash
pytest -q
AGENT_MODE=mock python run_evals.py
```

## Optional live model mode for the original agent app

```bash
export AGENT_MODE=live
export ANTHROPIC_API_KEY=YOUR_KEY
streamlit run app.py
```

Never commit API keys or a real `.streamlit/secrets.toml`.
