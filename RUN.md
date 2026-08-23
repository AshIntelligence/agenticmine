# Running Ash Intelligence locally

## Streamlit app

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
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

## Optional live model mode

```bash
export AGENT_MODE=live
export ANTHROPIC_API_KEY=YOUR_KEY
streamlit run app.py
```

Never commit API keys or a real `.streamlit/secrets.toml`.
