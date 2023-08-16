import js
from pyscript import Element
import json


class Output:
    id = ''
    text = ''
    def __init__(self, id):
        self.id = id


class Input:
    id = ''

    def __init__(self, id):
        self.id = id

    def value(self):
        if not Element(self.id).element:
            return ''
        elif Element(self.id).element.value == '':
            return ''
        else:
            return Element(self.id).element.value


class GeneralApp:
    name = 'General app'
    description = 'Default description'
    author = 'Andrew'
    okButton = {
        'text': 'Generate',
        'color': '#',
        'background': '#',
    }
    resetButton = {
        'text': 'Reset',
        'color': '#',
        'background': '#',
    }

    def __init__(self, api_key):
        self.api_key = api_key
        self.listInput = []
        self.listOutput = []

    def createInput(self, prompt, type):
        self.listInput.append({
            'id': len(self.listInput),
            'label': prompt
        })
        return Input(f'id-input-{len(self.listInput) - 1}')

    def createOutput(self, prompt):
        self.listOutput.append({
            'id': len(self.listOutput),
            'label': prompt
        })
        return Output(f'id-output-{len(self.listOutput) - 1}')

    def display(self, output, text):
        if not Element(output.id).element:
            js.console.log('not include')
        else:
            Element(output.id).element.value = text

    def build(self):
        js.console.log('build')
