import requests
import os
from .xclass_helpers import multipartify



class ChatBotApp:
  __apiKey = None
  __API_PATH="https://ptn4du8158.execute-api.ap-southeast-1.amazonaws.com/internal/chat-bot"
  name='Chat bot'
  description = 'Default description'
  author='Andrew'
  appLogo= 'https://i.postimg.cc/tT9pn3xQ/class-x-1.png'
  def __init__(self, apiKey):
    self.__apiKey = apiKey
  def build(self, filePath):
    absPath = os.path.abspath(filePath)
    url = self.__API_PATH
    headers = {
      'api-key': self.__apiKey,
    }
    with open(absPath, 'r', encoding='utf-8') as file:
            content = file.read()
            data = {
                'content': content,
                'name': self.name,
                'description': self.description,
                'appLogo': self.appLogo,
                'author': self.author,
            }
            response = requests.post(
                url, files=multipartify(data), headers=headers)
            print(response.json())