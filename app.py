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
from helpers import query_understanding,response_generating, ResponseGeneratingforAttendanceSummary
from hacknucleus import get_unsubmitted_tasks
from scavange_bunker import get_data
# from  flask_socketio import yield
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

def slave(llm, prompt):
    response = query_understanding(llm,prompt)
    print(response)
    tasks = None
    if response == "get_unsubmitted_tasks":
        tasks = get_unsubmitted_tasks()
        if(tasks):
            # print(tasks)
            yield response_generating(llm,tasks)
        else:
           yield  response_generating(llm,tasks)
            # print("something is terribly wrong")
    elif response ==  "attendance_summary":
        attendance = get_data()
        print(attendance)
        if attendance:
          yield ResponseGeneratingforAttendanceSummary(llm,attendance)
        else:
           yield  ResponseGeneratingforAttendanceSummary(llm,attendance)
        
# if(tasks):
    
