ADK (Multi-Agent) — Configuration and Run Notes

This folder contains the Python multi-agent ADK used by the FastAPI service. The ADK uses Google Generative AI (Gemini 2.5 Flash) for generation and the Google embeddings API when available.

Requirements

- Python dependencies: `google-generativeai`, `langchain_community`, `chromadb` (or whichever Chroma client you use), `uvicorn`, etc.
- Set the environment variable `GOOGLE_API_KEY` with a valid API key that has access to Gemini 2.5 Flash and the embeddings models.

Quick start (example)

```bash
cd modelserver-fastapi
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# install google generative sdk
pip install google-generativeai

# export your Google API key
export GOOGLE_API_KEY="YOUR_KEY_HERE"

# start FastAPI
uvicorn main:app --reload --port 8000
```

Test ADK endpoint

```bash
curl -X POST http://127.0.0.1:8000/adk_query -H "Content-Type: application/json" -d '{"query_text":"recommend me sci-fi movies like Interstellar"}'
```

Notes

- The ADK modules include intent routing, hybrid retrieval (semantic via Chroma + lexical via Express), re-ranking using IMDb-like rating, memory-based query rewriting, and generation. They are intended as a starting point and should be hardened for production (timeouts, rate-limits, retries, caching, security).
- If Google Gen SDK is not available at runtime, the ADK falls back gracefully and returns informative error messages in the `response` field.
