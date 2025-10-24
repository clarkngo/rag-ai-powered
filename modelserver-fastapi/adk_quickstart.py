"""Minimal FastAPI server implementing a Google ADK quickstart-style endpoint.

This provides a small, self-contained service with:
- GET /health -> basic health check
- POST /generate -> generate text with Google Generative AI SDK (Gemini) when available

Usage:
  export GOOGLE_API_KEY="..."
  uvicorn adk_quickstart:app --reload --port 9000

If the `google-generativeai` package is not installed or `GOOGLE_API_KEY` is missing,
the /generate endpoint will return a clear error explaining what's missing.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import logging
from dotenv import load_dotenv

# Load environment variables from a local .env file (if present). This lets
# developers put `GOOGLE_API_KEY=...` in `modelserver-fastapi/.env` or the repo
# root `.env` and not have to export it manually each session.
load_dotenv()

app = FastAPI(title="ADK Quickstart (minimal)")
logger = logging.getLogger("adk_quickstart")
logging.basicConfig(level=logging.INFO)

# Try to import the Google Generative AI SDK. We handle import failures gracefully and
# return helpful errors so developers can install packages and set creds.
HAS_GENAI = False
genai = None
try:
    import google.generativeai as genai  # type: ignore
    HAS_GENAI = True
except Exception as e:
    logger.info("google.generativeai not available: %s", e)
    HAS_GENAI = False


class GenerateRequest(BaseModel):
    prompt: str
    model: str | None = None  # allow overriding model; default chosen server-side
    max_tokens: int | None = 256


@app.get("/health")
async def health():
    """Simple health endpoint."""
    return {"status": "ok", "genai_installed": HAS_GENAI}


def _configure_genai_or_raise():
    """Configure the google-generativeai client or raise HTTPException with guidance."""
    if not HAS_GENAI:
        raise HTTPException(status_code=503, detail=(
            "google-generativeai is not installed in this environment. "
            "Install it with `pip install google-generativeai` and restart the server."))

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise HTTPException(status_code=503, detail=(
            "GOOGLE_API_KEY environment variable not set. "
            "Set it to a valid Google Cloud API key with GenAI access."))

    try:
        # configure the SDK; this will vary by SDK version but works in common releases
        genai.configure(api_key=api_key)
    except Exception as e:
        logger.exception("failed to configure google.generativeai: %s", e)
        raise HTTPException(status_code=500, detail=f"Failed to configure GenAI SDK: {e}")


@app.post("/generate")
async def generate(req: GenerateRequest):
    """Generate a text completion using the Google GenAI SDK (Gemini) when available.

    This endpoint is intentionally small — it demonstrates how to wire GenAI into a
    FastAPI route for quick local testing and iteration.
    """
    _configure_genai_or_raise()

    model_to_use = req.model or os.getenv("ADK_DEFAULT_MODEL", "gemini-2.5-flash")

    prompt = req.prompt
    logger.info("generate request model=%s len_prompt=%d", model_to_use, len(prompt))

    try:
        # The exact SDK call varies with google-generativeai versions. Many versions
        # expose a `generate_text` (or `generate`) function — we try a couple of
        # common names to be resilient across versions.
        response_text = None

        # Preferred: newer SDKs often provide `generate_text` or `generate` helpers.
        if hasattr(genai, "generate_text"):
            gen_resp = genai.generate_text(model=model_to_use, prompt=prompt, max_output_tokens=req.max_tokens)
            # gen_resp shape varies; try to extract text robustly
            response_text = getattr(gen_resp, "text", None) or gen_resp.get("output", {}).get("text") if isinstance(gen_resp, dict) else None

        if response_text is None and hasattr(genai, "generate"):
            gen_resp = genai.generate(model=model_to_use, input=prompt, max_output_tokens=req.max_tokens)
            # try common fields
            if isinstance(gen_resp, dict):
                # new SDK sometimes returns {'candidates': [{'content': '...'}], ...}
                candidates = gen_resp.get("candidates") or gen_resp.get("outputs")
                if candidates and isinstance(candidates, list) and len(candidates) > 0:
                    response_text = candidates[0].get("content") or candidates[0].get("text")

        # Last-resort: if the SDK has `TextGenerationModel` like interfaces, try safer access
        if response_text is None:
            # attempt to stringify the raw response
            response_text = str(gen_resp)

        return {"model": model_to_use, "response": response_text}

    except Exception as e:
        logger.exception("generation failed: %s", e)
        raise HTTPException(status_code=500, detail=f"Generation failed: {e}")
