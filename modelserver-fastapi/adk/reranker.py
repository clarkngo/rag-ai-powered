from typing import List, Dict

def normalize_rating(rating) -> float:
    try:
        r = float(rating)
        return max(0.0, min(r / 10.0, 1.0))
    except Exception:
        return 0.0

def rerank_results(semantic: List[Dict], lexical: List[Dict]) -> List[Dict]:
    """Combine semantic and lexical results and rerank using simple heuristics (imdb rating if available)."""
    items = []
    # normalize semantic items
    for s in semantic:
        m = s.get('metadata', {})
        imdb = m.get('imdb', {}) if isinstance(m.get('imdb', {}), dict) else {}
        rating = imdb.get('rating') if isinstance(imdb, dict) else None
        score = s.get('score', 0.0)
        items.append({'source':'semantic','content': s.get('content'), 'metadata': m, 'score': float(score), 'rating': normalize_rating(rating)})

    # add lexical results
    for l in lexical:
        movie = l.get('movie')
        rating = None
        if isinstance(movie.get('imdb', None), dict):
            rating = movie.get('imdb', {}).get('rating')
        items.append({'source':'lexical','content': movie.get('title',''), 'metadata': movie, 'score': float(l.get('score',0.0)), 'rating': normalize_rating(rating)})

    # compute combined score
    for it in items:
        # weight: 0.7 * normalized score + 0.3 * rating
        it['combined'] = 0.7 * (it.get('score') or 0.0) + 0.3 * (it.get('rating') or 0.0)

    items.sort(key=lambda x: x['combined'], reverse=True)
    return items
