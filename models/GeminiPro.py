import requests
from bs4 import BeautifulSoup
import json
from langchain_core.tools import tool
import getpass
import os
import dotenv, os, json

from google.oauth2 import service_account

from langchain_google_vertexai import ChatVertexAI
# from langchain_core.agents import Agent
# from langchain_core.agents.agent_toolkits import create_toolkit
# from langchain_core.agents.agent_executor import AgentExecutor
# from langchain_core.memory import ConversationBufferMemory

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
import os
# from langchain_gemini import ChatGemini
# from gemini import Gemini
class GeminiPro():
    def __init__(self):
        dotenv.load_dotenv()
        GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
        GCP_REGION = os.environ.get("GCP_REGION")
        GCP_CREDENTIALS_JSON = os.environ.get("GCP_CREDENTIALS_JSON")

        credentials = service_account.Credentials.from_service_account_info(json.loads(GCP_CREDENTIALS_JSON))
        scoped_creds = credentials.with_scopes(["https://www.googleapis.com/auth/cloud-platform"])

        self.llm = ChatVertexAI(
                model_name="gemini-pro",
                convert_system_message_to_human=False,
                project=GCP_PROJECT_ID,
                location=GCP_REGION,
                credentials=scoped_creds,
                max_output_tokens=8192,
                temperature=0.2,
        )
       
        self.output_parser = StrOutputParser()

        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Answer all questions to the best of your ability."),
            MessagesPlaceholder(variable_name="messages"),
        ])
        
        chain = self.prompt_template | self.llm | self.output_parser

        response = chain.invoke({
            "messages": [
                HumanMessage(content=prompt),
            ],
        })
        print(response)