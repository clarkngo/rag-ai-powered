import os
import requests
from typing import List, Dict

# Attempt to use Google's Generative AI SDK for embeddings (fallbacks handled)
try:
    import google.generativeai as genai
    genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))
    HAS_GOOGLE = True
except Exception:
    genai = None
    HAS_GOOGLE = False

CHROMA_PATH = 'chroma'
EXPRESS_URL = 'http://127.0.0.1:3000'


def get_embedding_function():
    """Return a callable that accepts a list of texts and returns a list of embeddings.

    Uses Google Generative SDK when available. If not available, returns a dummy
    embedding function (zero vectors) so callers don't crash.
    """
    if HAS_GOOGLE:
        def embed_texts(texts: List[str]):
            try:
                # Google Gen AI embeddings API may accept a single string or list
                resp = genai.embeddings.create(model='embed-gecko-001', input=texts)
                # resp may contain 'data' with embeddings
                if isinstance(resp, dict) and 'data' in resp:
                    return [item.get('embedding') for item in resp['data']]
                # attempt attribute access
                if hasattr(resp, 'data'):
                    return [getattr(d, 'embedding', None) for d in resp.data]
                return [[0.0]*768 for _ in texts]
            except Exception as e:
                print('embedding error', e)
                return [[0.0]*768 for _ in texts]

        return embed_texts

    else:
        def dummy(texts: List[str]):
            return [[0.0]*768 for _ in texts]

        return dummy


def semantic_search(query: str, k: int = 5) -> List[Dict]:
    """Perform semantic search using Chroma if available (requires chroma and embeddings).

    If Chroma or Google embeddings are not available, returns an empty list.
    """
    try:
        from langchain_community.vectorstores import Chroma
    except Exception:
        print('Chroma not available for semantic search')
        return []

    embedding_fn = get_embedding_function()
    try:
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_fn)
        results = db.similarity_search_with_score(query, k=k)
        return [{'content': doc.page_content, 'score': score, 'metadata': doc.metadata} for doc, score in results]
    except Exception as e:
        print('semantic_search error', e)
        return []


def lexical_search(query: str, k: int = 10) -> List[Dict]:
    """A simple lexical retriever that fetches movie documents from Express and performs token match locally."""
    try:
        resp = requests.get(f"{EXPRESS_URL}/movies?limit=500")
        resp.raise_for_status()
        movies = resp.json()
    except Exception as e:
        print('lexical_search error fetching movies:', e)
        movies = []

    q = query.lower().strip()
    matches = []
    tokens = [tok for tok in q.split() if tok]
    for m in movies:
        text = ' '.join([
            str(m.get('title', '')),
            ' '.join(m.get('genres', [])) if isinstance(m.get('genres', []), list) else str(m.get('genres', '')),
            ' '.join(m.get('cast', [])) if isinstance(m.get('cast', []), list) else str(m.get('cast', ''))
        ]).lower()
        if all(tok in text for tok in tokens):
            matches.append({'movie': m, 'score': 1.0})
    return matches[:k]
