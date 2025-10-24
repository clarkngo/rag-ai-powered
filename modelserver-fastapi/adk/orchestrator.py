from typing import List, Dict
from .intent_router import classify_intent
from .hybrid_retriever import semantic_search, lexical_search
from .reranker import rerank_results
from .memory_rewriter import rewrite_query
from .generator import generate_response

def run_multi_agent(query_text: str, chat_history: List[Dict]=None) -> Dict:
    """Run the multi-agent pipeline and return structured output.

    Output includes: intent, rewritten_query, semantic_results, lexical_results, reranked, final_response
    """
    intent = classify_intent(query_text)
    rewritten = rewrite_query(chat_history or [], query_text)

    # Retrieval
    semantic = semantic_search(rewritten, k=5)
    lexical = lexical_search(rewritten, k=10)

    # Rerank
    reranked = rerank_results(semantic, lexical)

    # Build a combined context (top N from reranked) for generation
    context_text = '\n\n---\n\n'.join([item.get('content') or str(item.get('metadata',{})) for item in reranked[:5]])

    # Generation
    final = generate_response(context_text, rewritten)

    return {
        'intent': intent,
        'rewritten_query': rewritten,
        'semantic_results': semantic,
        'lexical_results': lexical,
        'reranked': reranked,
        'response': final
    }
