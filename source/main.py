# source/main.py
from pathlib import Path

from source.utils import load_data, setup_vector_store, get_openai_client
from source.weakpoint_agent import weakpoint_detector 
from source.vector_searcher_agent import search_relevant_content
from source.study_planner import create_study_plan

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "Data" / "Student_rubric_feedback.csv"
OUT_PATH = ROOT / "personalized_study_plan.txt"

def main():
    print("Starting personalized study plan generation...")

    # 1) Load data
    print("Loading data…")
    df = load_data(str(DATA_PATH))

    # 2) Vector store + retriever
    print("Setting up vector store…")
    vector_store = setup_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    # 3) LLM (available if agents need it)
    llm = get_openai_client()  # noqa: F841

    # 4) Student -> list of feedback strings
    feedback = df.groupby("Student")["Feedback"].apply(list).to_dict()

    # 5) Agents (implemented by teammates)
    print("Analyzing weak points…")
    weakpoints = weakpoint_detector(feedback, retriever)
    print(weakpoints)

    print("Searching for relevant learning materials…")
    content_locations = search_relevant_content(weakpoints, retriever)

    print("Creating study plan…")
    study_plan = create_study_plan(weakpoints, content_locations, retriever)

    # 6) Output
    print("\n" + "=" * 50)
    print("STUDY PLAN GENERATED SUCCESSFULLY!")
    print("=" * 50)
    print(study_plan)

    OUT_PATH.write_text(study_plan, encoding="utf-8")
    print(f"\nSaved to {OUT_PATH}")

if __name__ == "__main__":
    main()
