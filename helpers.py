import json
from langchain_core.tools import tool
import os
from langchain_google_vertexai import ChatVertexAI
from dotenv import load_dotenv
load_dotenv()
import pytz
os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY')
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)
from datetime import datetime

def get_current_date_in_iso8601_format():
    """
    Gets the current date in the ISO 8601 format (YYYY-MM-DDTHH:MM:SS.000Z).

    Returns:
        str: The current date in the ISO 8601 format.
    """

  # Get the current UTC datetime
 
    india_tz = pytz.timezone('Asia/Kolkata')
    india_datetime = datetime.now(india_tz).strftime("%Y-%m-%d %H:%M:%S")
    return india_datetime




def query_understanding(llm,input):
    examples = [
        {"input": "Deii What should i do today", "output": "get_unsubmitted_tasks"},
        {"input": "What is it for me today", "output": "get_unsubmitted_tasks"},
        {"input":"What are the subject or courses my attendance is low? ","output":"attendance_low_summary"},
        {"input":"Can you tell me about my attendance?","output":"attendance_summary"},
        {"input":"how many classes I can take leave for Deep learning?","output":"attendance_specific(deep learning)"},
        {"input":"how many classes I can take leave for Functional Programming?","output":"attendance_specific(functional programming)"},
        {"input":"Deii? Im planning to bunk software testing! Whats my safe limit?","output":"attendance_specific(software testing)"},
        {"input":"how many classes I can take leave for Computer Vision?","output":"attendance_specific(computer vision)"},
        {"input":"Deii..? Whats my attendance status","output":"attendance_summary"}

    
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
            "You are a helpful assistant named Deii, that can generate the correct function name from [get_unsubmitted_tasks,attendance_specific,attendance_low_summary,attendance_summary] to call according to user query",
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
                You are a friendly helpful, Highly precise assistant named Deii,That summarixes the assigment data. The assignment data has The field daysRemanining, you must say with name that These are the days remaining for this assignment! along with a sweet and short description from description.
                Format the output as a user-friendly paragraph highlighting tasks due today and the number of days left for others. 
                if 'daysRemaining' is negative, this means that user has Failed to submit the assignemt on given deadline, 
                if its -20, it means that its 20 days after the completion of deadline
                do not give Dates AGAIN just give number of days remaining for the Yet to submit assignments. 
                [CORRECT NUMBER OF DAYS TO COMPLETE IS VERY MUCH IMPORTANT]! along with thier description! 
                Assignements whose deadline are completed must be said in last High preference must be given only for yet to submit (ie Deadline not yet exceeded) . if all tasks are deadline exceeded then just say you have only overdues , should be simple!
                If data is empty The response must be in the you are happy that user has Submitted all!
            """,
                ),
            # few_shot_prompt,
            ("human", "{data}"),
        ]
    )
    chain = final_prompt | llm
    print(data)
    content = chain.invoke(
        {
            "data":data,
            "date":get_current_date_in_iso8601_format()
            
        }
    )
    print(content.content)


def ResponseGeneratingforAttendanceSummary(llm,attendance):
    final_prompt = ChatPromptTemplate.from_messages(
        [
            (
          "system",
            """
                You are a friendly and helpful assistant named Deii, who analyzes attendance data and provides insights on the number of classes the user can bunk for each course. Your goal is to highlight the classes to bunk while cautioning the user if they have less than 2 classes to bunk for any course.

                1. **Classes to Bunk**: Clearly state the number of classes the user can bunk for each course.
                2. **Caution**: If the user has less than 2 classes to bunk for any course, provide a cautionary note emphasizing the importance of attending classes to maintain good attendance.
                3. **Attendance Percentage**: Include the attendance percentage for each course as additional information.

                Format the output as a concise and easy-to-understand paragraph, ensuring that the user can quickly grasp the key points.

                If the data is empty, respond positively, expressing happiness that the user has good attendance and no classes to bunk.
            """,
                ),
            # few_shot_prompt,
            ("human", "{data}"),
        ]
    )
    chain = final_prompt | llm
    content = chain.invoke(
        {
            "data":attendance,
            # "date":get_current_date_in_iso8601_format()
            
        }
    )
    print(content.content)

   