import os
try:
    import google.generativeai as genai
    genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))
    HAS_GOOGLE = True
except Exception:
    genai = None
    HAS_GOOGLE = False

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

def generate_response(context_text: str, question: str) -> str:
    """Generate a response using Google Gemini 2.5 Flash via the Google Gen SDK.

    Falls back with an informative message if the SDK or API key is missing.
    """
    prompt = PROMPT_TEMPLATE.format(context=context_text or '', question=question or '')
    if not HAS_GOOGLE:
        return '(generation-error) google generative sdk not installed or GOOGLE_API_KEY not set'

    try:
        # Use the text generation API; method names vary by SDK version.
        # Here we attempt to call the high-level generate_text API.
        resp = genai.generate_text(model='gemini-2.5-flash', prompt=prompt)
        # resp may expose text in different shapes depending on SDK
        if hasattr(resp, 'text'):
            return resp.text
        if isinstance(resp, dict):
            # attempt common response shapes
            candidates = resp.get('candidates') or resp.get('outputs')
            if candidates and isinstance(candidates, list):
                first = candidates[0]
                if isinstance(first, dict):
                    return first.get('content') or first.get('text') or str(first)
            return str(resp)
        return str(resp)
    except Exception as e:
        return f"(generation-error) {e}"
