import requests
from bs4 import BeautifulSoup
import json
from langchain_core.tools import tool
from langchain_core.agents import Agent
from langchain_core.agents.agent_toolkits import create_toolkit
from langchain_core.agents.agent_executor import AgentExecutor
from langchain_core.memory import ConversationBufferMemory
import os
from gemini import Gemini


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
else:
    print("Script tag not found")

@tool
def get_unsubmitted_tasks(tasks):
    """Returns a list of unsubmitted tasks."""
    return [task for task in tasks if task.submissions.submittedOn is None]


toolkit = create_toolkit(tools=[get_unsubmitted_tasks])
memory = ConversationBufferMemory(return_messages=True)
agent = Agent(toolkit, memory=memory)
executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=toolkit.tools)

gemini = Gemini(os.environ['GEMINI_API_KEY'], os.environ['GEMINI_API_SECRET'])

@gemini.bot('task_bot')
def task_bot(message, conversation, checkpoint):
    tasks = data.pageProps.query.data
    unsubmitted_tasks = getUnsubmittedTasks(tasks)
    if unsubmitted_tasks:
        response = f"You have the following unsubmitted tasks:\n{unsubmitted_tasks}"
    else:
        response = "You have no unsubmitted tasks."
    return response