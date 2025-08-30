# source/weakpoint_agent.py
from dotenv import load_dotenv

# The agent now takes the llm client as an argument
def weakpoint_detector(feedback, retriever, llm) -> str:
    # Get assignment prompt and rubric-related context
    context = retriever.invoke("What is the ad-hoc analysis assignment_prompt?")

    # Build a stronger, more structured prompt
    prompt = f"""
    You are Agent Weakpoint Detector. 
    You job is to utilize the {feedback} and connect to the {context} to create weakpoints that a user will need to study
    GOAL: Generate a list of SPECIFIC, ACTIONABLE weakpoints the student must work on.
    
    Rules:
    - Always ground your response in the instructor's feedback, rubric criteria, and assignment prompt.
    - Provide detailed explanations for *why* each weakpoint matters for each student.
    - If the feedback is vague, rely more heavily on rubric ratings and assignment requirements.
    - If the feedback is moderate, combine rubric + assignment prompt + instructor feedback.
    - If the feedback is detailed, leverage ALL available context to make weakpoints as specific as possible.
    - For each weakpoint, recommend concrete next steps the student can take to improve.

    """

    # Corrected API call using llm.invoke()
    resp = llm.invoke(prompt)

    raw_output = resp.content.strip()
    cleaned = raw_output.replace("\\n", "\n")
    return cleaned