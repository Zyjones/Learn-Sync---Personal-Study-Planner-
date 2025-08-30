# source/utils.py

import os
import pandas as pd
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv
import warnings

# Suppress the SyntaxWarning for invalid escape sequences
warnings.filterwarnings("ignore", category=SyntaxWarning)

# --- Configuration ---
PERSIST_DIR = "unified_chroma_db"
# Corrected list of course materials with a path relative to the project root
PDF_PATHS = [
    "Data/SQL slides/Advanced SQL I copy.pdf",
    "Data/SQL slides/Advanced SQL II copy.pptx.pdf",
    "Data/Assignment_prompt.pdf",
    "Data/Syllabus.pdf"
]
DATA_PATH = "Data/Student_rubric_feedback.csv"

# --- Core Functions ---

def load_data(filepath):
    """
    Loads and preprocesses the student rubric feedback data.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Data file not found: {filepath}")
    
    df = pd.read_csv(filepath, skipinitialspace=True)
    df.columns = df.columns.str.strip()
    return df

def load_documents():
    """
    Loads all PDF documents from the specified paths,
    splits them into pages, and adds source metadata.
    """
    all_docs = []
    for file_path in PDF_PATHS:
        # Check if the file exists before attempting to load it
        if os.path.exists(file_path):
            loader = PyPDFLoader(file_path)
            pages = loader.load_and_split()
            
            # Add source metadata to each page
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
    Initializes and returns the Chroma vector store.
    If the database doesn't exist, it creates it from the documents.
    """
    # Initialize embeddings (the OPENAI_API_KEY environment variable must be set)
    embeddings = OpenAIEmbeddings()
    
    # Check if the vector store already exists
    if os.path.exists(PERSIST_DIR) and os.path.isdir(PERSIST_DIR):
        print("Loading existing vector store.")
        vector_store = Chroma(
            persist_directory=PERSIST_DIR, 
            embedding_function=embeddings
        )
    else:
        print("Creating new vector store from documents.")
        docs = load_documents()
        vector_store = Chroma.from_documents(
            documents=docs, 
            embedding=embeddings, 
            persist_directory=PERSIST_DIR
        )
        vector_store.persist()
        
    return vector_store

def get_openai_client():
    """
    Initializes and returns a configured OpenAI Chat client.
    """
    load_dotenv()
    return ChatOpenAI(
        model='gpt-4o-mini',
        temperature=0.2,
        openai_api_key=os.getenv('OPENAI_API_KEY')
    )
    