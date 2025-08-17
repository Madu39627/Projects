 # main.py
from fastapi import FastAPI, HTTPException
from lesson_agent import LessonGenerationAgent
from dotenv import load_dotenv
import os
import requests
import json
from requests.auth import HTTPBasicAuth
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Initialize Lesson Generation Agent
lesson_agent = LessonGenerationAgent(gemini_api_key=os.getenv('GEMINI_API_KEY'))

# Define request models
class LessonParams(BaseModel):
    target_language: str
    primary_language: str
    proficiency_level: str
    lesson_focus: str
    learning_goals: str
    cultural_context: str
    age_group: str
    previous_performance: str = None

# API Endpoints
@app.get("/")
def read_root():
    return {"message": "Welcome to the Language Lesson API"}

@app.post("/generate-lesson")
def generate_lesson(lesson_params: LessonParams):
    """Generate a language lesson based on provided parameters"""
    try:
        lesson_content = lesson_agent.generate_lesson(lesson_params.dict())
        return lesson_content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/demo/public-api")
def demo_public_api():
    """Demo of public API requests"""
    # First example - GET list of posts
    url1 = "https://jsonplaceholder.typicode.com/posts"
    response1 = requests.get(url1)
    
    # Second example - GET single post
    url2 = "https://jsonplaceholder.typicode.com/posts/1"
    response2 = requests.get(url2)
    
    return {
        "multiple_posts": response1.json() if response1.status_code == 200 else f"Error: {response1.status_code}",
        "single_post": response2.json() if response2.status_code == 200 else f"Error: {response2.status_code}"
    }

@app.get("/demo/private-api")
def demo_private_api():
    """Demo of private API with authentication"""
    # Replace with your actual GitHub credentials or use environment variables
    github_username = os.getenv("GITHUB_USERNAME")
    token = os.getenv("GITHUB_TOKEN")
    
    if not github_username or not token:
        return {"error": "GitHub credentials not configured"}
    
    private_url = "https://api.github.com/user"
    response = requests.get(
        url=private_url,
        auth=HTTPBasicAuth(github_username, token))
    
    return {
        "status_code": response.status_code,
        "response": response.json() if response.status_code == 200 else f"Error: {response.status_code}"
    }

# Example usage when run directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)