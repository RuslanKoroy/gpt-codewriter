from constants import prompt_file, descriptions_file
from scripts.file_utils import get_block_list, get_current_block, get_block_content, get_notes
from scripts.gpt_utils import describe_file
import os
import json


def get_blocks_description():
    if os.path.exists(descriptions_file):
        with open(descriptions_file, encoding='utf8') as f:
            descriptions = json.load(f)
    else:
        descriptions = {}
    return descriptions


def get_static_prompt():
    with open(prompt_file, 'r', encoding='utf8') as f:
        prompt = f.read()
    return {'role': 'user', 'content': prompt}


def get_dynamic_prompt():
    prompt = ''
    blocks = get_block_list()
    descriptions = get_blocks_description()
    for block in blocks:
        prompt += '{' + block + '}\n'
        if block == get_current_block():
            prompt += f'```\n{get_block_content(block)}\n```\n\n'
        else:
            if block not in descriptions.keys():
                print(f'-- Warning: no description for block {block} --')
                descriptions[block] = 'empty block'
            description = descriptions[block]
            prompt += f'Block hidden. Use `unhide` command to switch to this block. Description: {description}\n\n'
    note, tasks = get_notes()
    if not note:
        note = 'empty'
    #tasks = '\n- '.join([t['task'] for t in tasks])
    task_list = ''
    for task in tasks:
        task_list += f'\n- Task {task["task_id"]}: {task["task"]}'
    prompt += f'Note: {note}\n\nTasks: {task_list}'
    if len(tasks) > 3:
        prompt += '\n\nNumber of tasks is greater than or equal to 4. Do not use the `add_task` command.'
    prompt += f'\n\nCurrent file: "{get_current_block()}"'
    return {'role': 'user', 'content': prompt}


def get_prompts():
    prompts = [get_static_prompt(), get_dynamic_prompt()]
    return prompts
