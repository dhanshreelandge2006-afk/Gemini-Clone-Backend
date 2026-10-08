from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()


genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

model = genai.GenerativeModel('gemini-3.8-flash')


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # Allows requests from specified origins
    allow_credentials=False,           # Allows cookies and authentication headers
    allow_methods=["*"],              # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],              # Allows all headers
)

class Prompt(BaseModel):
  text : str
  
@app.get('/')
def home():
  return {'message ': 'FastAPI server is running' }

@app.post('/generate')
def generate_response(prompt : Prompt):
  response = model.generate_content(prompt.text)
  return {
    'response' : response.text
  }