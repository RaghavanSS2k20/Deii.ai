import requests
from bs4 import BeautifulSoup
import json
from langchain_core.tools import tool
import os
from langchain_google_vertexai import ChatVertexAI
from dotenv import load_dotenv
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY')
from langchain_google_genai import ChatGoogleGenerativeAI
from helpers import query_understanding,response_generating
from hacknucleus import get_unsubmitted_tasks

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)
response = query_understanding(llm,"What is it for me today")
tasks = None
if response == "get_unsubmitted_tasks":
    tasks = get_unsubmitted_tasks()
    if(tasks):
        # print(tasks)
        response_generating(llm,tasks)
    else:
        print("something is terribly wrong")
# if(tasks):
    

    