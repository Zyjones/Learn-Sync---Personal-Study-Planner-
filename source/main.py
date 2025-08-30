# source/main.py
from dotenv import load_dotenv
load_dotenv()  # ensure .env is loaded before anything OpenAI/LangChain runs

from pathlib import Path
import os
import sys

from source.utils import load_data, setup_vector_store, get_openai_client
from source.weakpoint_agent import weakpoint_detector
from source.vector_searcher_agent import search_relevant_content
from source.study_planner import create_study_plan

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "Data" / "Student_rubric_feedback.csv"
OUT_DIR = ROOT / "Plans"
OUT_DIR.mkdir(exist_ok=True)

def main():
    print("Starting personalized study plan generation...")

    # 0) Sanity check: did we load the API key?
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY is not set. Check your .env and load_dotenv placement.", file=sys.stderr)
        sys.exit(1)

    # 1) Load data
    print("Loading data…")
    df = load_data(str(DATA_PATH))

    # Fix common column gotcha: 'Feedback ' -> 'Feedback'
    if "Feedback" not in df.columns and "Feedback " in df.columns:
        df = df.rename(columns={"Feedback ": "Feedback"})

    if "Student" not in df.columns:
        print("ERROR: Expected a 'Student' column in the CSV.", file=sys.stderr)
        sys.exit(1)
    if "Feedback" not in df.columns:
        print("ERROR: Expected a 'Feedback' column in the CSV.", file=sys.stderr)
        sys.exit(1)

    # 2) Vector store + retriever
    print("Setting up vector store…")
    vector_store = setup_vector_store()  # ensure this uses embeddings that read OPENAI_API_KEY
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    # 3) LLM (shared client)
    llm = get_openai_client()

    # 4) Group feedback per student
    feedback_map = df.groupby("Student")["Feedback"].apply(list).to_dict()

    for student, fb_list in feedback_map.items():
        print(f"\n=== {student}: analyzing weak points ===")
        # Join multiple feedback items into one string for the agent
        feedback_text = "\n".join(str(x) for x in fb_list if str(x).strip())

        # 5) Agents
        print("Analyzing weak points…")
        weakpoints = weakpoint_detector(feedback_text, retriever, llm)
        print(weakpoints)

        print("Searching for relevant learning materials…")
        content_locations = search_relevant_content(weakpoints, retriever, llm)

        print("Creating study plan…")
        study_plan = create_study_plan(weakpoints, content_locations, retriever, llm)

        # 6) Output per student
        out_path = OUT_DIR / f"{student}_study_plan.txt"
        out_path.write_text(study_plan, encoding="utf-8")
        print(f"Saved plan to {out_path}")

    print("\nAll plans generated.")

if __name__ == "__main__":
    main()
