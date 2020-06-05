import json
import requests
import os

github_key = os.getenv("REPO_GRAPHQL_TOKEN")
print(github_key)
repo_id = "MDEwOlJlcG9zaXRvcnkyNjkwNDA2MDA="

latest_message = """
    Latest Version splunk-8.0.4-767223ac207f-x64-release.msi available - Splunk Linux Addons
    NEW VERSION AVAILABLE - Splunk Universal Forwarder 8.0.4-767223ac207f
"""
title = "NEW VERSION AVAILABLE - Splunk Universal Forwarder"
latest_version_splunk_uf = "8.0.4-767223ac207f"

query = """query {
    characters {
        results {
            name
            status
            species
        }
    }
}"""

create_issue_mutation_string = f'''
    mutation {{
    __typename
    createIssue(input: {{repositoryId: "MDEwOlJlcG9zaXRvcnkyNjkwNDA2MDA=", title: "Splunk UF - New Version Available", body: "{latest_message}"}}) {{
    clientMutationId
    }}
}}'''

print(create_issue_mutation_string)

# response = requests.post(url, json={'query' : create_issue_mutation_string}, headers={"Authorization": "Bearer {}".format(github_key)})
def fetch_issues(repo_owner, repo_name):
  issue_list_query = f"""query {{
    repository(owner: "{repo_owner}", name: "{repo_name}") {{
      issues(first: 100) {{
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

  url = 'https://api.github.com/graphql'
  response = requests.post(url, json={'query' : issue_list_query}, headers={"Authorization": "Bearer {}".format(github_key)})
  response_dict = json.loads(response.text)
  return response_dict['data']['repository']['issues']['edges']

def should_raise(latest_version_splunk_uf, issues):
    first_time = True
    should_raise = True
    for item in issues:
      issue = item['node']
      if issue['title'] == "Splunk UF - New Version Available":
        first_time = False
        if latest_version_splunk_uf in issue['body']:
          should_raise = False

    if first_time or should_raise:
        return True

print(fetch_issues("bibbycodes", "github-api-test"))