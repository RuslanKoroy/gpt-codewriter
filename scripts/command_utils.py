import json
import re
import scripts.file_utils as fs


def handle_text(text):
    # Разбиваем текст на строки и парсим каждую команду
    commands = [parse_command(line) for line in text.split('\n')]
    for command in commands:
        if command['command'] == 'do_nothing':
            continue
        # Получаем функцию, соответствующую команде
        func = command_list[command['command']]
        args = command['args']
        # Вызываем функцию с аргументами
        try:
            func(**args)
            print(f'{command["command"]} with args {args}')
        except Exception as exception:
            print(f'Error in handle_text: {exception}')
    return commands


def parse_command(text):
    # Разбиваем текст на название команды и аргументы
    try:
        command_name, command_args = text.split(' ', 1)
        command_args = re.findall(r'{.*}', command_args)[0]
        command_args = json.loads(command_args)
        command_name = command_name.strip()
        if command_name not in command_list.keys():
            return {'command': 'do_nothing', 'args': {}}
        command = {
            'command': command_name,
            'args': command_args
        }
        return command
    except:
        return {'command': 'do_nothing', 'args': {}}


def add_task(task):
    note, tasks = fs.get_notes()
    if len(tasks) > 3:
        return
    task_id = len(tasks)
    tasks.append({'task': task, 'task_id': task_id})
    fs.save_notes(note, tasks)


def complete_task(task_id):
    note, tasks = fs.get_notes()
    for task in tasks:
        if task['task_id'] == task_id:
            tasks.remove(task)
    fs.save_notes(note, tasks)


def change_note(text):
    _, tasks = fs.get_notes()
    fs.save_notes(text, tasks)


# ключ - название команды, значение - соответствующая функция
command_list = {'create_file': fs.create_file,
    'delete_file': fs.delete_file,
    'unhide': fs.unhide,
    'add_line': fs.add_line,
    'edit_line': fs.edit_line,
    'delete_line':fs.delete_line,
    'execute': fs.execute,
    'do_nothing': print, 
    'add_task': add_task,
    'task_completed': complete_task, 
    'note': change_note,
    'add_text': fs.add_text}