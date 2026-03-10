from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Client using key from .env
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_gemini_treatment(disease_name):
    """Generates structured advice using Gemini 2.5 Flash."""
    if "Healthy" in disease_name:
        return "Your chilli plant is healthy! Continue regular watering and monitoring."

    prompt = f"""
    You are an agriculture expert helping Indian farmers.

    The chilli plant is infected with: {disease_name}.

    FOLLOW THIS EXACT FORMAT. DO NOT CHANGE HEADINGS. DO NOT USE ANY MARKDOWN formatting like **bold** stars. Write perfectly clean, raw text only.

    INTRO:
    Write 2 simple lines for the farmer.

    CAUSES:
   - cause 1/n
   - cause 2

   SYMPTOMS:
   - symptom 1
   - symptom 2

   PREVENTION:
   - prevention step
   - prevention step

  CHEMICAL:
  - pesticide name + doses

  ORGANIC:
  - organic method
"""

    try:
        # Using the 2.5 Flash model for speed and free tier access
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Gemini Advisory Error: {str(e)}"