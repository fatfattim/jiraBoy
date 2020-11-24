import requests
import jiraConfig
from requests.auth import HTTPBasicAuth
import json

url = jiraConfig.httpResource["url"]

headers = {
    "Authorization": jiraConfig.httpResource["authorization"],
    "Content-Type": "application/json"
}

def informByReleaseVersionList(releaseList):
    for release in releaseList:
      jql = "project = OTP AND issuetype != Release AND fixVersion = \""+release+"\""
      payload = json.dumps({
          "jql": jql,
          "fields": [
              "issuelinks"
          ],
          "startAt": 0,
          "maxResults": 20
      })
      response = requests.request(
          "POST",
          url,
          data=payload,
          headers=headers
      )

      jsonText = json.loads(response.text)
      jsonArray = jsonText['issues']
      #print(json.dumps(json.loads(response.text), sort_keys=True, indent=8, separators=(",", ": ")))
      print(release)
      for item in jsonArray:
        issueLinks = item['fields']['issuelinks']
        print(item['key'])
        if len(issueLinks) == 0:
          continue
        for issue in issueLinks:
            if 'outwardIssue' in issue:
                projectIssue = issue['outwardIssue']['key']
                if projectIssue.find('MM-') != -1:
                    print("-> Live Product: "+projectIssue)
                elif projectIssue.find('ST-') != -1:
                    print("-> Saku: "+projectIssue)
    

