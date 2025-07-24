import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load your API key from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use a lighter Gemini model
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# Load extracted resume data
with open("parsed_resume.json", "r", encoding="utf-8") as f:
    resume_data = json.load(f)

# Build prompt
prompt = f"""
You are a technical interviewer. Ask personalized interview questions based on the candidate's resume:

Name: {resume_data.get("name")}
Email: {resume_data.get("email")}
Phone: {resume_data.get("phone")}
LinkedIn: {resume_data.get("linkedin")}
GitHub: {resume_data.get("github")}
Education: {', '.join(resume_data.get("education", []))}
Skills: {', '.join(resume_data.get("skills", []))}
Experience: {', '.join(resume_data.get("experience", []))}
Projects: {', '.join(resume_data.get("projects", []))}

Generate 5 personalized technical interview questions based on this profile.
"""

# Generate questions
response = model.generate_content(prompt)
questions = response.text.strip().split("\n")

# Save interview questions
with open("interview_questions.txt", "w", encoding="utf-8") as f:
    f.write(response.text.strip())
print("✅ Interview questions saved to interview_questions.txt")

# Load answers from transcribed file
with open("transcribed_answers.txt", "r", encoding="utf-8") as f:
    answers = [line.strip() for line in f if line.strip()]

# Combine questions and answers into a report
with open("transcript.txt", "w", encoding="utf-8") as f:
    f.write(f"👤 Candidate: {resume_data.get('name')}\n\n")
    for i, (q, a) in enumerate(zip(questions, answers), 1):
        f.write(f"Q{i}: {q.strip()}\n")
        f.write(f"A{i}: {a.strip()}\n\n")

print("✅ Transcript saved to transcript.txt")
