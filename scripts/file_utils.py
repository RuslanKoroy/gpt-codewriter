import os
import json
import chardet
from constants import notes_file, workspace_folder, descriptions_file, exec_result_file, block_size
from scripts.gpt_utils import describe

current_block: str = ""

def set_current_block(block: str):
    global current_block
    current_block = block

def get_current_block():
    return current_block

project_path: str = ""


def current_path():
    return os.path.join(workspace_folder, project_path, current_block.split(':')[0])


def remove_files():
    if os.path.exists(notes_file):
        os.remove(notes_file)
    if os.path.exists(descriptions_file):
        os.remove(descriptions_file)


def set_project_path(path):
    global project_path
    project_path = path
    if not os.path.exists(get_path('')):
        os.makedirs(get_path(''))


def get_notes():
    try:
        with open(notes_file, encoding='utf8') as f:
            notes = json.load(f)
        note = notes['note']
        tasks = notes['tasks']
    except FileNotFoundError:
        note = ""
        tasks = []
    return note, tasks


def save_notes(note, tasks):
    notes = {'note': note, 'tasks': tasks}
    with open(notes_file, 'w+', encoding='utf8') as f:
        json.dump(notes, f, ensure_ascii=False)


def get_block_list():
    block_list = []
    path = os.path.join(workspace_folder, project_path)
    # проходимся по всем папкам и файлам в указанной директории и ее подпапках
    for root, dirs, files in os.walk(path):
        # игнорируем папки venv, .git, .idea и прочие системные файлы и папки
        dirs[:] = [d for d in dirs if d not in ['venv', '.git', '.idea']]
        for file in files:
            if file.endswith(('.py', '.md', '.json', '.js', '.html', '.css')):
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as f:
                    content = f.read()
                    if len(content) > block_size:
                        blocks = [content[i:i+block_size] for i in range(0, len(content), block_size)]
                        for i, block in enumerate(blocks):
                            key = f"{os.path.relpath(file_path, path)}:{i}"
                            block_list.append(key)
                    else:
                        key = os.path.relpath(file_path, path) + ':0'
                        block_list.append(key)
    with open('block_list.md', 'w+', encoding='utf8') as f:
        f.write('\n'.join([block for block in block_list]))
    check_block_descriptions(block_list)
    return block_list



def check_block_descriptions(block_list):
    descriptions: dict = {}
    if not os.path.exists(descriptions_file):
        with open(descriptions_file, 'w+') as file:
            file.write('{}')
    else:
        with open(descriptions_file, 'r', encoding='utf8') as f:
            try:
                descriptions = json.load(f)
            except (json.JSONDecodeError, ValueError):
                descriptions = {}
    for block in block_list:
        if block not in descriptions.keys():
            describe_block(block)


# функция получает название блока и возвращает блок заданного номера из файла
def get_block_content(block):
    filename, block_number = block.split(':')
    with open(get_path(filename), 'r', encoding='utf-8') as f:
        content = f.read()
        if not content:
            return ''
        blocks = [content[i:i+block_size] for i in range(0, len(content), block_size)]
        if int(block_number) >= len(blocks):
            return ''
        block_content = blocks[int(block_number)].split('\n')
        block_content = [f'{i}~{line}' for i, line in enumerate(block_content)]
        block_content = '\n'.join(block_content)
        return block_content


def describe_block(block):
    text = get_block_content(block)
    description = 'empty file'
    if text:
        description = describe(text)
    descriptions: dict = {}
    if not os.path.exists(descriptions_file):
        with open(descriptions_file, 'w+') as file:
            file.write('{}')
    else:
        with open(descriptions_file, 'r', encoding='utf8') as f:
            try:
                descriptions = json.load(f)
            except (json.JSONDecodeError, ValueError):
                descriptions = {}
    descriptions[block] = description
    with open(descriptions_file, 'w+', encoding='utf8') as f:
        json.dump(descriptions, f, ensure_ascii=False)


# функция для создания файла
def create_file(path):
    with open(get_path(path), "w", encoding="utf8") as f:
        f.write('')
    set_current_block(path + ':0')
    describe_block(path + ':0')


# функция для удаления файла
def delete_file(path):
    path = get_path(path)
    if os.path.exists(path):
        os.remove(path)
    else:
        print("Файл не найден")


def split_to_blocks(text, filename):
    # делим текст на блоки по block_size символов
    blocks = [text[i:i+block_size] for i in range(0, len(text), block_size)]

    blocks_dict = {}
    for i, block in enumerate(blocks):
        key = f"{filename}:{i+1}"
        blocks_dict[key] = block

    return blocks_dict


# функция для отображения скрытого блока кода
def unhide(block):
    describe_block(current_block)
    set_current_block(block)
    return


# функция для добавления строки в файл
def add_line(number, line):
    with open(current_path(), "r", encoding="utf8") as f:
        text = f.readlines()
    text.insert(number - 1, line + "\n")
    with open(current_path(), "w", encoding="utf8") as f:
        f.writelines(text)


# функция для добавления текста в файл
def add_text(text):
    with open(current_path(), "r", encoding="utf8") as f:
        file_text = f.read()
    file_text += '\n' + text
    with open(current_path(), "w", encoding="utf8") as f:
        f.write(file_text)
    block_list = get_block_list()
    last_block = 0
    for block in block_list:
        if block.startswith(current_path()):
            if int(block.split(':')[1]) > last_block:
                last_block = int(block.split(':')[1])
                set_current_block(block)


# функция для замены содержимого строки в файле
def edit_line(number, line):
    with open(current_path(), "r", encoding="utf8") as f:
        text = f.readlines()
    text[number - 1] = line + "\n"
    with open(current_path(), "w", encoding="utf8") as f:
        f.writelines(text)


# функция для удаления строки из файла
def delete_line(number):
    # получаем информацию о файлах из json файла
    with open(current_path(), "r", encoding="utf8") as f:
        text = f.readlines()
    # удаляем строку из списка
    del text[number - 1]
    # записываем изменения в файл
    with open(current_path(), "w", encoding="utf8") as f:
        f.writelines(text)


def get_code_result(encoding='cp1251'):
    if not os.path.exists(exec_result_file):
        return "the code didn't output anything."
    with open(exec_result_file, encoding=encoding) as file:
        text = file.read()
    with open(exec_result_file, 'w+', encoding=encoding) as file:
        file.write('')
    return text


# функция для выполнения кода из файла
def execute(path):
    # Запускаем файл в зависимости от его расширения
    if path.endswith(".py"):
        os.system(f"python {path} > {exec_result_file} 2>&1")
    else:
        os.system(f"{path} > {exec_result_file} 2>&1")
        print(f"Участок кода {i + 1} имеет неизвестный формат файла.")


def get_path(path):
    return os.path.join(workspace_folder, project_path, path)

