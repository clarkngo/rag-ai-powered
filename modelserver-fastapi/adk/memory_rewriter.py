from typing import List

def rewrite_query(history: List[dict], query: str) -> str:
    """Rewrite the query by adding context from the last turns if the query is short/ambiguous.

    history: list of { role: 'user'|'assistant', text: str }
    """
    if not history or not isinstance(history, list):
        return query

    q = (query or '').strip()
    if len(q.split()) > 6:
        return q  # likely self-contained

    # find last user turn
    last_user = None
    for entry in reversed(history):
        if entry.get('role') == 'user' and entry.get('text'):
            last_user = entry.get('text')
            break

    if last_user:
        return f"In context of: \"{last_user}\". Question: {q}"

    return q
