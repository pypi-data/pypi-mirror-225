import requests
import json
from .xclass_helpers import multipartify



class ProfileApp:
  __apiKey = None
  __API_PATH="https://ptn4du8158.execute-api.ap-southeast-1.amazonaws.com/dev/profile"
  def __init__(self, apiKey):
    self.__apiKey = apiKey
  def buildProfile(self, class_name='class_name', **kwargs):
    url = self.__API_PATH
    headers = {
      'api-key': self.__apiKey,
    }
    data=dict(**kwargs)

    data["class"] = class_name
    if "education" in data:
      for edu in data["education"]:
        edu["from"] = edu["from_time"]
        edu["to"] = edu["to_time"]
      data["education"] = json.dumps(data["education"])
    if "prizes" in data:
      data["prizes"] = json.dumps(data["prizes"])
    if "links" in data:
      data["links"] = json.dumps(data["links"])
    if "futurePlan" in data:
      data["futurePlan"] = json.dumps(data["futurePlan"])
    response = requests.post(url, files=multipartify(data), headers=headers)
    print(response.json())