import os
import json
from google import genai
from google.genai.types import HttpOptions
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from your .env file!")

client = genai.Client(api_key=GEMINI_API_KEY,
            http_options=HttpOptions(api_version="v1"))

def generate_questions(role: str, job_description: str, resume_text: str, count: int = 5) -> list[str]:

    print("=== AVAILABLE GEMINI MODELS ===")
    try:
        for m in client.models.list():
            print(m.name)
    except Exception as e:
        print(f"Failed to list models: {e}")
    print("===============================")
    prompt = f"""
    You are an expert technical interviewer. Generate exactly {count} tailored technical interview questions 
    for a candidate applying for the role of: {role}.

    Candidate Context:
    - Job Description: {job_description}
    - Candidate Resume Highlights: {resume_text[:1000]}

    Requirements:
    1. Focus on practical, role-relevant questions balancing theory and real-world scenarios.
    2. Format the output strictly as a valid JSON array of strings. 
    3. Do NOT include markdown formatting (like ```json), return raw JSON text only.

    Example Output Format:
    ["Question 1?", "Question 2?", "Question 3?"]
    """
# THESE Prompts WILL HELP THE AI TO GENERATE QUESTIONS AND USER DON'T HAVE TO WRITE COMPLEX LLM INSTRUCTIONS  


    try:
        response = client.models.generate_content(
            model='models/gemini-2.5-flash',
            contents=prompt
        )


        raw_text = response.text.strip()

        if raw_text.startswith("```"):
            raw_text = raw_text.split("\n", 1)[1].rsplit("\n", 1)[0].strip()

        questions_list = json.loads(raw_text)
        return questions_list

    except Exception as e:
        print(f"Gemini API Error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate questions using Gemini AI."
        )