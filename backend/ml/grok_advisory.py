import os
from openai import OpenAI

# Initialize Grok Client
client = OpenAI(
    api_key=", 
    base_url="https://api.x.ai/v1",
)

def get_grok_advisory(disease_name):
    if "Healthy" in disease_name:
        return "Your chilli plant is healthy! Keep up the good work."

    prompt = f"""
    Act as a professional Indian Agronomist. 
    Provide a detailed advisory for the chilli plant disease: {disease_name}.
    
    Format the output exactly like this:
    CAUSE: (Why did it happen?)
    SYMPTOMS: (What does it look like?)
    CHEMICAL TREATMENT: (India-specific pesticides/fungicides)
    ORGANIC TREATMENT: (Neem oil, etc.)
    PREVENTION: (How to avoid next time?)
    """

    response = client.chat.completions.create(
        model="grok-4-fast", # Or "grok-beta"
        messages=[
            {"role": "system", "content": "You are a helpful agricultural expert."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    
    return response.choices[0].message.content