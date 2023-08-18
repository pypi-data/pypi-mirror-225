import js
from pyscript import Element
import json


class MathApp:
    def __init__(self, api_key):
        self.api_key = api_key
        self.listInput = []

    def createInput(self, prompt):
        self.listInput.append({
        'id': len(self.listInput),
        'label': prompt
        })
        return f'id-{len(self.listInput) - 1}'

    def getValue(self, input_id):
        if not Element(input_id).element:
            return 0
        elif Element(input_id).element.value == '':
            return 1
        else:
            return Element(input_id).element.value

    def display(self, message, value):
        Element('result').write(f"{message} {value}")

    def build(self):
        js.console.log(json.dumps(self.listInput))
