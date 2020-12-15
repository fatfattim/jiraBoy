import requests
import jiraConfig
from requests.auth import HTTPBasicAuth
import json
import informProjectTeam
import re

'''
To list the roadmap with different component
'''

url = jiraConfig.httpResource["url"]

headers = {
    "Authorization": jiraConfig.httpResource["authorization"],
    "Content-Type": "application/json"
}

payload = json.dumps({
    "jql": "project = OTP AND parentEpic = OTP-2023 ORDER BY created DESC",
    "fields": [
        "customfield_10007", #sprint field
        "components"
    ],
    "startAt": 0,
    "maxResults": 30
})

response = requests.request(
    "POST",
    url,
    data=payload,
    headers=headers
)

jsonText = json.loads(response.text)
jsonArray = jsonText['issues']
sprintListOutput = {}

# you can print the response from below codes
for item in jsonArray:
  sprintList = item['fields']['customfield_10007']
  components = item['fields']['components']
  if sprintList is None:
      continue
  componentNameList = []
  for component in components:
      componentNameList.append(component['name'])
  
  for sprint in sprintList:
      sprintName = sprint['name']
      if sprintName in sprintListOutput:
        firstList = sprintListOutput[sprintName]
        # Merge and remove duplicated components
        sprintListOutput[sprintName] = list(set(firstList+componentNameList))
      else:
        sprintListOutput[sprintName] = componentNameList
    #sprintListOutput.append(sprint['name'])

Output = {}
for x in sprintListOutput:
  pattern = re.compile("(PlayBoy Sprint [0-9]*)")
  result = pattern.search(x)
  if result is None:
    continue
  else:
    Output[result.group()] = sprintListOutput[x]

keylist = Output.keys()
keylist = sorted(keylist)

for key in keylist:
    print(key)

for key in keylist:
    print(str(Output[key]))

#print(keylist)
#print(json.dumps(json.loads(response.text), sort_keys=True, indent=8, separators=(",", ": ")))