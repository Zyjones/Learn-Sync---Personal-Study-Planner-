# source/vector_searcher_agent.py

def search_relevant_content(weakpoints, retriever, llm) -> dict:
  """
  This agent will look into the vector database to connect the weakpoints to the course materials.
  """
  # Grab context for the weakpoints
  context = retriever.invoke("What is the ad-hoc analysis assignment_prompt?")

  # Create a prompt for Agent Vector Searcher
  prompt = f""" 
  You are Agent Vector Searcher. You job is to utilize the {weakpoints} and {context} to give us clusters of where the information is at (for example, Join information are in Advanced SQL I copy slides 10-12)
  I want the output as a dictionary
  Example: Student 1 Weakpoint: Information Located
  
  """
  # Corrected API call using llm.invoke()
  resp = llm.invoke(prompt)
  cleaned = resp.content.strip()
  return cleaned