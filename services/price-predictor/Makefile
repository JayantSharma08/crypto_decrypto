reset-venv:
	uv clean
	rm -rf .venv
	rm uv.lock
	uv sync
	
training:
	uv run python training.py

inference:
	uv run python inference.py
