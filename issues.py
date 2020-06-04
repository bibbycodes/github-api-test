import json
import requests
import os

github_key = os.getenv("REPO_GRAPHQL_TOKEN")
print(github_key)
repo_id = "MDEwOlJlcG9zaXRvcnkyNjkwNDA2MDA="

query = """query {
    characters {
        results {
            name
            status
            species
        }
    }
}"""

create_issue_mutation_string = """mutation {
    __typename
    createIssue(input: {repositoryId: "MDEwOlJlcG9zaXRvcnkyNjkwNDA2MDA=", title: "Splunk UF - New Version Available", body: "this is a test body"}) {
    clientMutationId
    }
}"""

issue_list_query_string = """query {
    repository(owner: "bibbycodes", name: "github-api-test") {
    issues(first: 100) {
      edges {
        node {
          body
          title
          state
        }
      }
    }
  }
}"""

url = 'https://api.github.com/graphql'

response = requests.post(url, json={'query' : issue_list_query_string}, headers={"Authorization": "Bearer {}".format(github_key)})
response_dict = json.loads(response.text)
issues = response_dict['data']['repository']['issues']['edges']

for item in issues:
    issue = item['node']
    if issue['state'] == "OPEN":
        print(issue)

