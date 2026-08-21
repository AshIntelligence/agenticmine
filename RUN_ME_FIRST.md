# Run the portfolio locally — fastest path

## Windows: double-click

1. Clone or download this repository.
2. Make sure Python 3.11 or 3.12 is installed and **Add Python to PATH** was checked during installation.
3. Double-click **`run_windows.bat`**.
4. The first run creates `.venv`, installs dependencies, and opens the demo at **http://localhost:8501**.

The launcher intentionally uses **mock mode**. The orchestration, retrieval, scoring, evals, traces, and UI execute for real; only the external model response is deterministic so an interview demo cannot fail because of Wi‑Fi, an API key, or billing.

## PowerShell alternative

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\run_windows.ps1
```

## Manual commands

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:AGENT_MODE="mock"
streamlit run app.py
```

Then open **http://localhost:8501**.

## Run proof checks

```powershell
python run_evals.py
pytest -q
```

Expected:
- **4/4 golden behavioral evals passing**
- **3/3 unit tests passing**

## Optional live Claude mode

```powershell
$env:AGENT_MODE="live"
$env:ANTHROPIC_API_KEY="YOUR_KEY"
$env:ANTHROPIC_MODEL="claude-sonnet-5"
streamlit run app.py
```

Never commit your API key.
