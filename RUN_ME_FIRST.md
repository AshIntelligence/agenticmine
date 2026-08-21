# Run the portfolio locally

## Windows: fastest path

1. Clone or download this repository.
2. Install Python 3.11 or 3.12 and enable **Add Python to PATH**.
3. Double-click **`run_windows.bat`**.
4. The launcher creates `.venv`, installs dependencies, uses deterministic mock mode, and opens **http://localhost:8501**.

Mock mode keeps the orchestration, retrieval, scoring, evals, traces, and UI real while making model output deterministic and reproducible.

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

## Run tests and evals

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
