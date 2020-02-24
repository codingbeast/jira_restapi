import requests
import json

#get the user information from the accessible-resources
def resources(access_token):
    url = "https://api.atlassian.com/oauth/token/accessible-resources"
    payload = {}
    headers = {
        'Authorization': 'Bearer {0}'.format(access_token)
        }
    response = requests.request("GET", url, headers=headers, data = payload)
    data=response.json()[0]
    return data


#get project details from the project rest api using get method
#7626d1e6-9f89-4733-be7e-9998dd39cb52
#COD
def projects(access_token,client_id):
    url = "https://api.atlassian.com/ex/jira/{0}/rest/api/2/project/search".format(client_id)
    payload = {}
    headers = {
        'Authorization': 'Bearer {0}'.format(access_token)
        }
    response = requests.request("GET", url, headers=headers, data = payload).json()['values']
    return response

def getIssues(access_token,project_code,client_id):
    url = "https://api.atlassian.com/ex/jira/{0}/rest/api/2/search?jql=project='{1}'".format(client_id,project_code)
    payload = {}
    headers = {
        'Authorization': 'Bearer {0}'.format(access_token)
        }
    response = requests.request("GET", url, headers=headers, data = payload).json()['issues']
    return response
def isssueadd(access_token,client_id,project_code,summary,description,issueType):
    url="https://api.atlassian.com/ex/jira/{0}/rest/api/2/issue".format(client_id)
    headers = {
              'Content-Type' : 'application/json',
              'Authorization' : 'Bearer {0}'.format(access_token),
               }
    parameters={
    "fields": {
       "project":
       {
          "key": project_code
       },
       "summary": summary,
       "description": description,
       "issuetype": {
          "name": issueType
       }
   
        }
    }
    p={}
    response = requests.post(url, headers = headers, data =json.dumps(parameters), params =  parameters)
    return response
def getIssueType(access_token,client_id,project_id):
    url="https://api.atlassian.com/ex/jira/{0}/rest/api/2/project/{1}".format(client_id,project_id)
    payload = {}
    headers = {
        'Authorization': 'Bearer {0}'.format(access_token)
        }
    response = requests.request("GET", url, headers=headers, data = payload).json()['issueTypes']
    issuenames=[i['name'] for i in response]
    return issuenames
    