import argparse
import os
import shutil
import os
try:
    import google.generativeai as genai
    genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))
    HAS_GOOGLE = True
except Exception:
    genai = None
    HAS_GOOGLE = False

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.document_loaders import PyPDFDirectoryLoader

import requests
import pymongo

CHROMA_PATH = "chroma"
DATA_PATH = "data"

def get_embedding_function():
    # Return a callable that takes a list of texts and returns embeddings.
    if HAS_GOOGLE:
        def embed_texts(texts):
            try:
                resp = genai.embeddings.create(model='embed-gecko-001', input=texts)
                if isinstance(resp, dict) and 'data' in resp:
                    return [item.get('embedding') for item in resp['data']]
                if hasattr(resp, 'data'):
                    return [getattr(d, 'embedding', None) for d in resp.data]
            except Exception as e:
                print('embedding error', e)
            # fallback
            return [[0.0]*768 for _ in texts]

        return embed_texts

    else:
        def dummy(texts):
            return [[0.0]*768 for _ in texts]
        return dummy

def load_documents_from_database():
    response = requests.get('http://127.0.0.1:3000/movies-sample')
    movies = response.json() 

    documents = []
    for movie in movies:
        if 'title' in movie and 'plot' in movie:
            print(movie['title'])
            text = f"{movie['title']} {movie['plot']}"  
            documents.append(Document(page_content=text, metadata={'movie_id': movie['_id']}))

    return documents

def load_documents_from_data_folder():
    document_loader = PyPDFDirectoryLoader(DATA_PATH)
    return document_loader.load()

def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)

def calculate_chunk_ids(chunks):

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id

    return chunks

def add_to_chroma(chunks: list[Document]):
    # Load the existing database.
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()
    )

    # Calculate Page IDs.
    chunks_with_ids = calculate_chunk_ids(chunks)

    # Add or Update the documents.
    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
        db.persist()
        print(f"✅ Finished adding new documents: {len(new_chunks)}")
    else:
        print("✅ No new documents to add")


def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

def main():
    # Check if the database should be cleared (using the --clear flag).
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    if args.reset:
        print("✨ Clearing Database")
        clear_database()

    # Create (or update) the data store.
    # documents = load_documents_from_database()
    documents = load_documents_from_data_folder()
    chunks = split_documents(documents)
    add_to_chroma(chunks)

if __name__ == "__main__":
    main()
