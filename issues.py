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

issue_query = """mutation {
    __typename
    createIssue(input: {repositoryId: "MDEwOlJlcG9zaXRvcnkyNjkwNDA2MDA=", title: "this is a test issue creation"}) {
    clientMutationId
    }
}"""

url = 'https://api.github.com/graphql'

r = requests.post(url, json={'query' : issue_query}, headers={"Authorization": "Bearer {}".format(github_key)})
print(r.text)