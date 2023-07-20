'''import librarries'''
import re
import os
import xml.etree.ElementTree as ET
import openai

def connect_to_openai():
    '''method to connect with OpenAI API'''
    openai.organization = "org-WTPCAZdWARkJoItCjU9VV1WE"
    openai.api_key = ""
    openai.Model.list()
    model_name = "gpt-3.5-turbo"
    return model_name

def get_response(model_input, instruction, hint_input):
    '''method to request suggestion from OpenAI API'''
    response = openai.ChatCompletion.create(
        model=model_input,
        messages=[
            {"role": "system", "content": instruction},
            {"role": "user", "content": hint_input},
        ],
        temperature=0,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response['choices'][0]['message']['content']

def enterprise_finetuning(code_input, match_replace):
    '''method to finetune the suggested code for enterprise'''
    for match in match_replace:
            if str(match) !='{}':
                for key, value in match.items():
                    if key in code_input:
                        code_input=code_input.replace(key, value)
    return code_input

def get_config_match(match_input, match_replace):
    '''method to finetune the suggested code for enterprise'''
    match=''
    for match in match_replace:
            if str(match) !='{}':
                for key, value in match.items():
                    if key == match_input:
                        match=value
    return match

def read_lang_config(tag_value, lang_input):
    '''method to read language configurations'''
    current_dir = os.path.dirname(__file__)
    tree = ET.parse(current_dir + "/" + lang_input + "-config.xml")
    root = tree.getroot()
    match_replace_list=[{}]
    for child in root:
        match_dict=child.attrib
        match = match_dict.get(tag_value)
        replace=child.text
        match_replace={match: replace}
        match_replace_list.append(match_replace)
    return match_replace_list


def remove_passwords(hint):
    pattern = r"\b[A-Za-z0-9@#$%^&+=]{8,}\b"
    return re.sub(pattern, "password", hint)

def remove_api_keys(hint):
    pattern = r"[A-Za-z0-9]{32}"
    return re.sub(pattern, "sample-key-", hint)

def remove_bank_details(hint):
    pattern = r"\b(?:\d{4}-){3}\d{4}\b|\b(?:\d{4} ){3}\d{4}\b|\b(?:\d{4}\.){3}\d{4}\b"
    return re.sub(pattern, "", hint)

def remove_personal_details(hint):
    pattern = r'\b(\d{4}-\d{2}-\d{2}|\d{3}-\d{2}-\d{4}|(\d{3}\s?){3}|\d{4}\s\d{4}\s\d{4}\s\d{4})\b'
    return re.sub(pattern, '[REDACTED]', hint)

def code_suggest(lang, hint):
    MODEL = connect_to_openai()
    LANG = lang
    attrib = read_lang_config("match", LANG)
    hint_prefix=get_config_match('hint_prefix', attrib)
    INSTRUCTION = "only code in " + LANG + ", do not elaborate, do not provide example or comment"
    HINT = hint_prefix + hint
    #HINT=hint
    #HINT = remove_api_keys(HINT)
    #HINT = remove_passwords(HINT)
    code = get_response(MODEL, INSTRUCTION, HINT)
    #attrib = read_lang_config("match", LANG)
    enterprise_name=get_config_match('instructions', attrib)
    #code = enterprise_name + '\n' + code
    #attrib = read_lang_config("match", LANG)
    code=enterprise_finetuning(code, attrib)
    LANG='enterprise'
    attrib = read_lang_config("match", LANG)
    code=enterprise_finetuning(code, attrib)
    return code

code = code_suggest('sql','get second highest salary record from table emp')
code = code_suggest('sql','rewrite this query in optimized form ' + code )
print(code)
