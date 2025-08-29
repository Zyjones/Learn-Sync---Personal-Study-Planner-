#AI Agent: Vector Searcher:
  #This agent will look into the vector database to connect the weakpoints to the content

  #give us clusters of where the information is at (for example, Join information are in Advanced SQL I copy slides 10-12)
  #Output (Dictionary?)
    #Student 1 Weakpoint: Information Located
    #

def vector_Searcher(weakpoints: dict) -> dict:
  #This agent will look into the vector database to connect the weakpoints to the content

  #Grab context for the weakpoints
  context = vector_retriever.get_relevant_documents("What is the ad-hoc analysis assignment_prompt?")
  

  #Create a prompt for Agent Weakpoint Detector
  prompt = f""" 
  You are Agent Weakpoint Detector. You job is to utilize the {weakpoints} and {context} to give us clusters of where the information is at (for example, Join information are in Advanced SQL I copy slides 10-12)
  I want the output as a dictionary
  Example: Student 1 Weakpoint: Information Located
  
  """
  # get back answer from `gpt-4o-mini` using context & prompt
  resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
  cleaned = resp.choices[0].message.content.strip()
  #print(cleaned)
  return cleaned