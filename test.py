import requests
from bs4 import BeautifulSoup
import json
from langchain_core.tools import tool
# from langchain_core.agents import Agent
# from langchain_core.agents.agent_toolkits import create_toolkit
# from langchain_core.agents.agent_executor import AgentExecutor
# from langchain_core.memory import ConversationBufferMemory
import os
# from langchain_gemini import ChatGemini
# from gemini import Gemini


url = "https://nucleus.amcspsgtech.in/"

def login(data):
    authUrl = url+"oauth"
    try:
        response = requests.post(authUrl, json=data)
        cookies = response.cookies
        cookie_dict = {}
        for cookie_name, cookie_value in cookies.items():
            cookie_dict[cookie_name] = cookie_value
            # print(f"{cookie_name}: {cookie_value}")
        return cookie_dict
    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")


def hackNucleus(cookies):
    try:
        hackUrl = url+"assignments"
        response = requests.get(hackUrl, cookies=cookies)
        soup = BeautifulSoup(response.text,'html.parser')
        return soup
    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")
        return None


def getData():
    data = {
        "rollNo":"20PW26",
        "password":"raghavan"
    }
    cookies = login(data)
    res = hackNucleus(cookies)
    # print(res)
    script_tag = res.find('script', {'id': '__NEXT_DATA__'})

    if script_tag:
        data = json.loads(script_tag.contents[0])
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)
        # print(data, type(data))
        return data
    else:
        print("Script tag not found")
        return None


def get_unsubmitted_tasks():
    """
        Returns a list of unsubmitted tasks.

        Properties:
            - type: string
            - description: A list of color names
            - no params needed
    """

    tasks = getData()
    tasks = tasks["props"]["pageProps"]["query"]["data"]
    if tasks:
        return [
            {
                "name" : task["title"],
                "description" : task["description"],
                "deadline":task["targetDateTime"],
                "courseName" : task["courseName"]
            } 
            for task in tasks if task["submissions"]["submittedOn"] is None]
    else:
        return ["fool"]


# toolkit = create_toolkit(tools=[get_unsubmitted_tasks])
# memory = ConversationBufferMemory(return_messages=True)
# agent = Agent(toolkit, memory=memory)
# executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=toolkit.tools)

# gemini = Gemini(os.environ['GEMINI_API_KEY'], os.environ['GEMINI_API_SECRET'])

# @gemini.bot('task_bot')
# def task_bot(message, conversation, checkpoint):
#     tasks = data.pageProps.query.data
#     unsubmitted_tasks = getUnsubmittedTasks(tasks)
#     if unsubmitted_tasks:
#         response = f"You have the following unsubmitted tasks:\n{unsubmitted_tasks}"
#     else:
#         response = "You have no unsubmitted tasks."
#     return response


import getpass
import os
# import dotenv, os, json

from google.oauth2 import service_account

from langchain_google_vertexai import ChatVertexAI
from dotenv import load_dotenv
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY')
# llm = ChatVertexAI(model="gemini-1.5-pro")
# result = llm.invoke("Write a ballad about Gemini Pro in around 3 sentences.")
# print(get_unsubmitted_tasks())

from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)
# get_unsubmitted_tasks_tool = llm.as_tool(get_unsubmitted_tasks)

from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
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
# messages = [
#     (
#         "system",
#         "You are a helpful assistant named Deii, that can generate the correct function name from [get_unsubmitted_tasks, get_user_name, get_course_name] to call according to user query",
#     ),
#     ("human", "What is it for me today"),
#     ("human", "get_unsubmitted_tasks"),
#     ("human", "Deii What should i do today"),
#     ("human", "get_unsubmitted_tasks"),
# ]

chain = final_prompt | llm
messages = chain.invoke({"input": "Today whats the drill?"})
print(messages)

if(messages.content.strip(' \n') == "get_unsubmitted_tasks"):
    print("Ok")
    tasks = get_unsubmitted_tasks()
    input_text = "How many days are remaining for the following tasks?"
    context = ""
    for task in tasks:
        context += f"{task['name']} in {task['courseName']} is due on {task['deadline']}\n"
    prompt_template = ChatPromptTemplate.from_template("""
        What is it today? Please summarize my tasks for the next 2 days.
        """)
    prompt = prompt_template.format_messages(text=input_text, context=context)
    print(prompt)
    output_text = llm.invoke(prompt)
    input_text = "Summarize the following output:"
    context = output_text.content

    # output_text = llm(input_text, context=context)

    print(output_text)
