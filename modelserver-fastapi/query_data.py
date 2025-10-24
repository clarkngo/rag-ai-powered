import argparse
import argparse
from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFDirectoryLoader

from adk.generator import generate_response
from adk.hybrid_retriever import semantic_search

CHROMA_PATH = "chroma"
DATA_PATH = "data"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

def query_rag(query_text: str):
    # Prepare the DB.
    results = semantic_search(query_text, k=5)

    context_text = "\n\n---\n\n".join([r.get('content','') for r in results])
    response_text = generate_response(context_text, query_text)

    sources = [r.get('metadata', {}).get('id', None) for r in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    return response_text


def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)

if __name__ == "__main__":
    main()
