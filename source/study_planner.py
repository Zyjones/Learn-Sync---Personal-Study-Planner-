# source/study_planner.py

def create_study_plan(weakpoints, assignment_location, retriever, llm):
    """
    This function will create an agent that will create a 7 day study plan based on weakpoints and where the information is located using gpt-4o-mini language model. 
    
    Argument: 
        student weakpoints and assigment location, retriever 

    Returns:
        return the output of the large language model expressed as a dictionary of study plans per student 
    """

    #Context for the agent 
    context = retriever.invoke("What's on the syllabus?")

    #Create a prompt for Agent Study Planner
    prompt = f"""
    You are Agent Study Planner. Your job is to create a 7 day study plan for each student based on {weakpoints} and include where the information is located {assignment_location} as resources: 
    A good study plan consist of SMART Goals, Spaced repetition & retrieval practice. Each day include a time block dedicated to studying that specific skill. Make a 7 day plan for each student based on their own feedback.
    Break the time blocks into 30 minutes sessions with a break in the middle
    Return as a dictionary
    Student 1: 
    Monday: Work on SQL problems. Resources = File Name: Slides 10-12
    Tuesday: Practice Join statements . Resources = Slides 5-6 Inner joins 
    """
  
    # Corrected API call using llm.invoke()
    resp = llm.invoke(prompt)
    
    cleaned = resp.content.replace("\\n", "\n")
    return cleaned