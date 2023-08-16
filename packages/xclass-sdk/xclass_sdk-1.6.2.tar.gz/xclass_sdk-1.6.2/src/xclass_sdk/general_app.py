import json
import requests
from .xclass_helpers import multipartify


class Output:
    label = 'Output'
    text = ''
    def __init__(self, label):
        self.label = label
class Input:
    lable = 'Input'
    text = ''
    def __init__(self, label):
        self.lable = label
    def value(self):
        return 1
    
class GeneralApp:
    __apiKey = None
    __API_PATH = "https://ptn4du8158.execute-api.ap-southeast-1.amazonaws.com/dev/general-app"
    name='General app'
    description = 'Default description'
    author='Andrew'
    isProd = True
    slug=''
    appLogo= 'https://uploads-ssl.webflow.com/64b02318b9d14ab16e20227a/64b3fda42fdf5ab7222c5a80_logo-xclass.png'
    okButton={
        'text':'Generate',
        'color': '#ea850c',
        'background':'linear-gradient(to bottom right, #ffedd5, #fdba74)',
    }
    resetButton={
        'text':'Reset',
        'color': '#000000',
        'background':'#EFEFEF',
    }
    def __init__(self, api_key, isProd=True):
        self.__apiKey = api_key
        self.isProd = isProd
        self.listInput = []
        self.listOutput = []
    def createInput(self, prompt, type):
        self.listInput.append({
        'id': f'id-input-{len(self.listInput)}',
        'label': prompt,
        'type': type
        })
        return Input(prompt)
    def createOutput(self, prompt):
        self.listOutput.append({
        'id': f'id-output-{len(self.listOutput)}',
        'label': prompt,
        })
        return Output(prompt)
    
    def display(self, output, text):
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
                'outputs':json.dumps(self.listOutput),
                'content': content,
                'okButton': json.dumps(self.okButton),
                'resetButton': json.dumps(self.resetButton),
                'name': self.name,
                'description': self.description,
                'appLogo': self.appLogo,
                'author': self.author,
                'slug': self.slug,
                'browserSdkPath': 'https://app.xclass.edu.vn/prod/general_app.py' if self.isProd else 'https://app.xclass.edu.vn/dev/general_app.py'  
            }
            response = requests.post(
                url, files=multipartify(data), headers=headers)
            print(response.json())