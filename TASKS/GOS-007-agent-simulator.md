# GOS-007: Agent Simulator & Model Adapters

## Objective
Build simulated agent runners and local model adapters (Ollama, LM Studio, llama.cpp, Local OpenAI-compatible) along with Guardian AI classifier and offline fallback.

## Deliverables
1. Model adapters in `models/adapters/` (`base.py`, `ollama.py`, `lmstudio.py`, `llamacpp.py`, `openai_compat.py`).
2. Guardian AI classifier in `models/adapters/guardian.py` evaluating injection/threat likelihood, with fail-secure offline fallback.
3. Simulation runner in `simulations/agent_simulator.py`.
4. Unit tests in `tests/unit/test_model_adapters.py`.
