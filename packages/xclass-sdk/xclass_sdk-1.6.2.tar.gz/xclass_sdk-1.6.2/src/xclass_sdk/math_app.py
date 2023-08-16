import json
import requests
from .xclass_helpers import multipartify

class MathApp:
    __apiKey = None
    __API_PATH = "https://ptn4du8158.execute-api.ap-southeast-1.amazonaws.com/dev/math-app"
    def __init__(self, api_key):
        self.__apiKey = api_key
        self.listInput = []
    def createInput(self, prompt):
        self.listInput.append({
        'id': f'id-{len(self.listInput)}',
        'label': prompt
    })
        return prompt

    def getValue(self, input_id):
        return 1

    def display(self, message, value):
        return 0

    def build(self, filePath):
        url = self.__API_PATH
        headers = {
            'api-key': self.__apiKey,
        }
        with open(filePath, 'r') as file:
            content = file.read()
            data = {
                'inputs': json.dumps(self.listInput),
                'content': content
            }
            response = requests.post(
                url, files=multipartify(data), headers=headers)
            print(response.json())