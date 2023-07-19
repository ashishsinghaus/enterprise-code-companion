'''import librarries'''
import os
import xml.etree.ElementTree as ET
import openai

def connect_to_openai():
    '''method to connect with OpenAI API'''
    openai.organization = "org-WTPCAZdWARkJoItCjU9VV1WE"
    openai.api_key = "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"
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


def code_suggest(lang, instructions, hint):
    MODEL = connect_to_openai()
    LANG = lang
    INSTRUCTION = "only code in " + LANG + ", do not elaborate, do not provide example or comment" + instructions
    HINT = hint
    code = get_response(MODEL, INSTRUCTION, HINT)
    INSTRUCTION = "elaborate"
    '''description = get_response(MODEL, INSTRUCTION, "Elaborate " + HINT)'''
    attrib = read_lang_config("name", LANG)
    code=enterprise_finetuning(code, attrib)
    return code

'''code = code_suggest('sql','','Write a query to find top 10 rows in a table')
print(code)'''
