
from dotenv import load_dotenv
from openai import OpenAI

def weakpoint_detector(feedback, retriever) -> str:
    # Get assignment prompt and rubric-related context
    context = retriever.get_relevant_documents("What is the ad-hoc analysis assignment_prompt?")
    

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

    # Call OpenAI API with slightly higher temperature for more detail
    client = OpenAI()
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    raw_output = resp.choices[0].message.content.strip()
    cleaned = raw_output.replace("\\n", "\\n")
    return cleaned

# Calling the function:
#weakpoints = weakpoint_detector(feedback, retriever)
#print(weakpoints)