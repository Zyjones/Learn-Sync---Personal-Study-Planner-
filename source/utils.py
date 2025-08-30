# source/utils.py

import os
import warnings
import pandas as pd
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

# Suppress the SyntaxWarning for invalid escape sequences
warnings.filterwarnings("ignore", category=SyntaxWarning)

# --- Configuration ---
PERSIST_DIR = "unified_chroma_db"
PDF_PATHS = [
    "Data/SQL slides/Advanced SQL I copy.pdf",
    "Data/SQL slides/Advanced SQL II copy.pptx.pdf",
    "Data/Assignment_prompt.pdf",
    "Data/Syllabus.pdf",
]
DATA_PATH = "Data/Student_rubric_feedback.csv"

# --- Core Functions ---

def load_data(filepath: str) -> pd.DataFrame:
    """Load and preprocess the student rubric feedback data."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Data file not found: {filepath}")
    df = pd.read_csv(filepath, skipinitialspace=True)
    df.columns = df.columns.str.strip()
    return df

def load_documents():
    """
    Load all PDF documents from the specified paths,
    split them into pages, and add source metadata.
    """
    all_docs = []
    for file_path in PDF_PATHS:
        if os.path.exists(file_path):
            loader = PyPDFLoader(file_path)
            pages = loader.load_and_split()
            for page in pages:
                page.metadata["source_name"] = file_path
            all_docs.extend(pages)
        else:
            print(f"File not found: {file_path}")
    if not all_docs:
        raise FileNotFoundError("No PDF documents were loaded. Please check your file paths.")
    return all_docs

def setup_vector_store():
    """
    Initialize and return the Chroma vector store.
    If the database doesn't exist, create it from the documents.
    Requires OPENAI_API_KEY to be present in the environment.
    """
    # Use env-loaded key (loaded in main.py)
    embeddings = OpenAIEmbeddings(  # optionally set model="text-embedding-3-small"
        # openai_api_key=os.getenv("OPENAI_API_KEY")  # not required if env is set
    )

    if os.path.exists(PERSIST_DIR) and os.path.isdir(PERSIST_DIR):
        print("Loading existing vector store.")
        vector_store = Chroma(
            persist_directory=PERSIST_DIR,
            embedding_function=embeddings,
        )
    else:
        print("Creating new vector store from documents.")
        docs = load_documents()
        vector_store = Chroma.from_documents(
            documents=docs,
            embedding=embeddings,               # works; or embedding_function=embeddings
            persist_directory=PERSIST_DIR,
        )
        vector_store.persist()

    return vector_store

def get_openai_client():
    """
    Return a shared LangChain ChatOpenAI client.
    .env must already be loaded in main.py.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set. Ensure load_dotenv() runs in main.py and .env exists.")
    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2,
        openai_api_key=api_key,
    )

