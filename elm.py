import os
import openai
import xml.etree.ElementTree as ET

openai.organization = "org-WTPCAZdWARkJoItCjU9VV1WE"
openai.api_key = "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"
openai.Model.list()
MODEL = "gpt-3.5-turbo"

def get_response(prompt):
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Reply with only code snippets in python, do not elaborate, do not show eaxample, do not include comments"},
            {"role": "user", "content": str(prompt)},
        ],
        temperature=0,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response['choices'][0]['message']['content']

def resolve_enterprise_vulnerability(tag_value, code):
    if tag_value in code:
        code = code.replace(tag_value, "")
    return code

def read_enterprise_config(name):
    tree = ET.parse('config.xml')
    root = tree.getroot()
    value = root[0].text
    return value

hint = "#write a program to generate prime numbers in python"
tag_value = read_enterprise_config("name")
hint=resolve_enterprise_vulnerability(tag_value, hint)
code = get_response(hint)
code = hint + "\n" + code

print(code)
