import os
import openai
import xml.etree.ElementTree as ET

def connect_to_openai():
    openai.organization = "org-WTPCAZdWARkJoItCjU9VV1WE"
    openai.api_key = "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"
    openai.Model.list()
    MODEL = "gpt-3.5-turbo"
    return MODEL


def get_response(hint, MODEL, lang):
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Reply with only  " + lang + ", do not elaborate, do not show eaxample, do not include comments"},
            {"role": "user", "content": hint},
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
    tree = ET.parse('enterprise-config.xml')
    root = tree.getroot()
    value = root[0].text
    return value


if __name__ == "__main__":
    MODEL = connect_to_openai()
    hint = "# write a program to generate prime numbers in python"
    lang = "sql"
    tag_value = read_enterprise_config("name")
    hint=resolve_enterprise_vulnerability(tag_value, hint)
    code = get_response(hint, MODEL, lang)
    code = hint + "\n" + code
    print(code)