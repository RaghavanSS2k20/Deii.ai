import requests
from bs4 import BeautifulSoup
import json
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
        return []


