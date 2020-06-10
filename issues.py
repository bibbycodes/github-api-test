import json
import requests
import os

github_key = os.getenv("REPO_GRAPHQL_TOKEN")
repo_id = "MDEwOlJlcG9zaXRvcnkyNjkwNDA2MDA="
latest_message = """
    Latest Version splunk-10.0.4-767223ac207f-x64-release.msi available - Splunk Linux Addons
    NEW VERSION AVAILABLE - Splunk Universal Forwarder 10.0.4-767223ac207f
"""
title = "NEW VERSION AVAILABLE - Splunk Universal Forwarder"
latest_version = "11.0.4-767223ac207f"

print(latest_version in latest_message)

def create_issue(repo_id, title, body):
  url = 'https://api.github.com/graphql'
  create_issue_mutation = f'''
      mutation {{
      __typename
      createIssue(input: {{repositoryId: "{repo_id}", title: "{title}", body: "{body}"}}) {{
      clientMutationId
      }}
  }}'''

  return requests.post(url, json={'query' : create_issue_mutation}, headers={"Authorization": "Bearer {}".format(github_key)})

def fetch_issues(repo_owner, repo_name):
  """Returns all issues' body, title and state for a given repo on github"""

  issue_list_query = f"""query {{
    repository(owner: "{repo_owner}", name: "{repo_name}") {{
      issues(last: 10) {{
        edges {{
          node {{
            body 
            title
            state
          }}
        }}
      }}
    }}
  }}"""

  issue_list_query_by_label = f"""{{
  repository(owner: "{repo_owner}", name: {repo_name}") {{
    issues(last: 10, filterBy: {{labels: "SplunkUFVersion"}}) {{
      edges {{
        node {{
          title
          }}
        }}
      }}
    }}
  }}"""

  url = 'https://api.github.com/graphql'
  response = requests.post(url, json={'query' : issue_list_query}, headers={"Authorization": "Bearer {}".format(github_key)})
  response_dict = json.loads(response.text)
  return response_dict['data']['repository']['issues']['edges']

def should_raise(latest_version, issues):
  """Loops through all issues in repo, if latest splunk version not in issues, returns True"""
  first_time = True
  latest_version_in_body = False
  for item in issues:
    issue = item['node']
    if issue['title'] == "NEW VERSION AVAILABLE - Splunk Universal Forwarder":
      first_time = False
      if latest_version in issue['body']:
        latest_version_in_body = True

  if first_time or not latest_version_in_body:
    return True
  return False

issues = fetch_issues("bibbycodes", "github-api-test")
if should_raise(latest_version, issues):
  print(create_issue(repo_id, title, latest_message).text)
else:
  print("Not Raising Issue")