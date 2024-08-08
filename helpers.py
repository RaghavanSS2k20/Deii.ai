import json
from langchain_core.tools import tool
import os
from langchain_google_vertexai import ChatVertexAI
from dotenv import load_dotenv
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY')
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)
import datetime

def get_current_date_in_iso8601_format():
  """
  Gets the current date in the ISO 8601 format (YYYY-MM-DDTHH:MM:SS.000Z).

  Returns:
    str: The current date in the ISO 8601 format.
  """

  # Get the current UTC datetime
  now = datetime.datetime.utcnow()

  # Format the datetime as an ISO 8601 string
  iso8601_str = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

  return iso8601_str



def query_understanding(llm,input):
    examples = [
        {"input": "Deii What should i do today", "output": "get_unsubmitted_tasks"},
        {"input": "What is it for me today", "output": "get_unsubmitted_tasks"},
    
    ]
    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{input}"),
            ("ai", "{output}"),
        ]
    )
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=examples,
    )
    final_prompt = ChatPromptTemplate.from_messages(
        [
            (
            "system",
            "You are a helpful assistant named Deii, that can generate the correct function name from [get_unsubmitted_tasks, get_user_name, get_course_name] to call according to user query",
                ),
            few_shot_prompt,
            ("human", "{input}"),
        ]
    )
    chain = final_prompt | llm
    messages = chain.invoke(input)
    return messages.content.strip(' \n')

def response_generating(llm,data):
    examples = [
        {"input": " [{'name': 'CLASSIFICATION AND REGRESSION USING PERCEPTRON', 'description': '-', 'deadline': '2024-07-22T03:11:00.000Z', 'courseName': 'DEEP LEARNING LAB'}, {'name': '20XW97 COMPUTER VISION LAB TASK 2', 'description': '20XW97 COMPUTER VISION AND IMAGE ANALYSIS LAB TASK 2', 'deadline': '2024-07-25T17:30:00.000Z', 'courseName': 'COMPUTER VISION LAB'}, {'name': 'SOFTWARE TESTING LAB TEST I', 'description': 'SOFTWARE TESTING LAB TEST I :: SUBMIT YOUR CODE ALONG WITH TEST CASES AND OUTPUT ', 'deadline': '2024-08-02T04:45:00.000Z', 'courseName': 'SOFTWARE TESTING'}, {'name': 'COMPUTER VISION AND IMAGE ANALYSIS LAB TASK 3', 'description': 'COMPUTER VISION AND IMAGE ANALYSIS LAB TASK 3', 'deadline': '2024-08-06T17:30:00.000Z', 'courseName': 'COMPUTER VISION LAB'}, {'name': 'Functional Programming Lab PROBLEMSHEET 2', 'description': 'Functional Programming Lab PROBLEMSHEET 2', 'deadline': '2024-08-05T17:30:00.000Z', 'courseName': 'FUNCTIONAL PROGRAMMING LAB'}]", "output": "Oops you are out of schedule!!"},
        {"input": " [{'name': 'CLASSIFICATION AND REGRESSION USING PERCEPTRON', 'description': '-', 'deadline': '2024-07-22T03:11:00.000Z', 'courseName': 'DEEP LEARNING LAB'}, {'name': '20XW97 COMPUTER VISION LAB TASK 2', 'description': '20XW97 COMPUTER VISION AND IMAGE ANALYSIS LAB TASK 2', 'deadline': '2024-07-25T17:30:00.000Z', 'courseName': 'COMPUTER VISION LAB'}, {'name': 'SOFTWARE TESTING LAB TEST I', 'description': 'SOFTWARE TESTING LAB TEST I :: SUBMIT YOUR CODE ALONG WITH TEST CASES AND OUTPUT ', 'deadline': '2024-08-02T04:45:00.000Z', 'courseName': 'SOFTWARE TESTING'}, {'name': 'COMPUTER VISION AND IMAGE ANALYSIS LAB TASK 3', 'description': 'COMPUTER VISION AND IMAGE ANALYSIS LAB TASK 3', 'deadline': '2024-08-16T17:30:00.000Z', 'courseName': 'COMPUTER VISION LAB'}, {'name': 'Functional Programming Lab PROBLEMSHEET 2', 'description': 'Functional Programming Lab PROBLEMSHEET 2', 'deadline': '2024-08-07T17:30:00.000Z', 'courseName': 'FUNCTIONAL PROGRAMMING LAB'}]", "output": "get_unsubmitted_tasks"},
    
    ]
    final_prompt = ChatPromptTemplate.from_messages(
        [
            (
            "system",
            """
                You are a friendly helpful, precise assistant named Deii, Calculate the number of days remaining for each task in the provided data, all time calculations must be based on Indian timezone current date in india is {date}. Format the output as a user-friendly paragraph highlighting tasks due today and the number of days left for others. do not give Dates AGAIN just give number of days remaining for the Yet to submit assignments. [NUMBER OF DAYS TO COMPLETE IS VERY MUCH IMPORTANT]! along with thier description! 
                Assignements whose deadline are completed must be said in last High preference must be given only for yet to submit (ie Dead line not yet exceeded)
            """,
                ),
            # few_shot_prompt,
            ("human", "{data}"),
        ]
    )
    chain = final_prompt | llm
    
    content = chain.invoke(
        {
            "data":data,
            "date":get_current_date_in_iso8601_format()
            
        }
    )
    print(content.content)


