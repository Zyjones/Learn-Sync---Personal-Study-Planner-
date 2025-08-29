# source/utils.py
import os
from pathlib import Path
import pandas as pd
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# Repo root no matter where this module is imported from
ROOT = Path(__file__).resolve().parents[1]

def load_data(filepath: str) -> pd.DataFrame:
    """Load CSV and do light cleanup."""
    df = pd.read_csv(filepath, skipinitialspace=True)
    df.columns = df.columns.str.strip()
    return df

def _pdf_paths():
    """Absolute paths to the PDFs we want in the vector DB."""
    return [
        ROOT / "Data" / "SQL slides" / "Advanced SQL I copy.pdf",
        ROOT / "Data" / "SQL slides" / "Advanced SQL II copy.pptx.pdf",
        ROOT / "Data" / "Assignment_prompt.pdf",
        ROOT / "Data" / "Syllabus.pdf",
    ]

def setup_vector_store():
    """
    Build or open a persistent Chroma vector store with OpenAI embeddings.
    If the DB already exists, we open it; otherwise we create it from PDFs.
    """
    persist_dir = ROOT / "vectordb_index"
    collection_name = "learnsync"

    embeddings = OpenAIEmbeddings()  # needs OPENAI_API_KEY in .env

    # If a DB already exists, open it without re-adding docs (avoids duplicates)
    if persist_dir.exists() and any(persist_dir.iterdir()):
        return Chroma(
            collection_name=collection_name,
            persist_directory=str(persist_dir),
            embedding_function=embeddings,
        )

    # Otherwise, load PDFs and create the DB
    docs = []
    for p in _pdf_paths():
        if not p.exists():
            print(f"[warn] Missing PDF: {p}")
            continue
        loader = PyPDFLoader(str(p))
        pages = loader.load_and_split()
        for page in pages:
            page.metadata["source_name"] = p.name
        docs.extend(pages)

    return Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=str(persist_dir),
        collection_name=collection_name,
    )

def get_openai_client():
    """Small helper to get the LLM if any agent needs it."""
    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
    )
