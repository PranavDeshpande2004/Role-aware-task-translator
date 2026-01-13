# import requests
# import os

# JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
# JIRA_EMAIL = os.getenv("JIRA_EMAIL")
# JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")


# def get_jira_issue(issue_key: str):
#     url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}"

#     print("JIRA URL:", url)
#     print("JIRA EMAIL:", JIRA_EMAIL)
#     print("JIRA TOKEN PRESENT:", bool(JIRA_API_TOKEN))

#     response = requests.get(
#         url,
#         auth=(JIRA_EMAIL, JIRA_API_TOKEN),
#         headers={"Accept": "application/json"}
#     )

#     print("JIRA STATUS:", response.status_code)
#     print("JIRA RESPONSE:", response.text)

#     if response.status_code != 200:
#         raise Exception("Failed to fetch Jira issue")

#     data = response.json()

#     title = data["fields"]["summary"]

#     description = ""
#     desc_field = data["fields"].get("description")
#     if desc_field and "content" in desc_field:
#         description = desc_field["content"][0]["content"][0]["text"]

#     return title, description



import requests
import os

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

def get_jira_issue(issue_key: str):
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}"

    #  Auth & headers MUST be defined
    auth = (JIRA_EMAIL, JIRA_API_TOKEN)
    headers = {
        "Accept": "application/json"
    }

    response = requests.get(url, auth=auth, headers=headers)

    if response.status_code != 200:
        print("JIRA STATUS:", response.status_code)
        print("JIRA RESPONSE:", response.text)
        raise Exception("Failed to fetch Jira issue")

    data = response.json()
    fields = data.get("fields", {})

    # Title
    title = fields.get("summary", "")

    # description parsing
    description = ""
    desc = fields.get("description")

    if desc and "content" in desc:
        try:
            description = desc["content"][0]["content"][0]["text"]
        except (IndexError, KeyError, TypeError):
            description = ""

    return title, description
