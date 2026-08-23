.PHONY: demo eval test app

demo:
	AGENT_MODE=mock python demo.py all

eval:
	AGENT_MODE=mock python run_evals.py

test:
	AGENT_MODE=mock pytest -q

app:
	streamlit run app.py
