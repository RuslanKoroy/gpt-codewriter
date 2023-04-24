from scripts.prompt_utils import get_prompts
from scripts.command_utils import handle_text
from scripts.generate_text import generate_message
from scripts.file_utils import create_file, get_code_result, current_block, set_project_path, remove_files


# Функция для выполнения команды, переданной в качестве аргумента
def execute_command(command):
    commands = {
        'create_file': create_file,
        'get_code_result': get_code_result,
        'current_block': current_block,
        'set_project_path': set_project_path,
        'remove_files': remove_files,
        'exit': exit
    }
    cmd, *args = command.split()
    # Если команда существует в словаре, то она выполняется
    if cmd in commands:
        commands[cmd](*args)
    else:
        print(f'Unknown command: {cmd}')


def log_prompts(prompts):
    with open('prompt_log.md', 'w+', encoding='utf8') as f:
        f.write('\n\n'.join([prompt['content'] for prompt in prompts]))


def log_gpt_response(response):
    with open('gpt_responses.md', 'a+', encoding='utf8') as file:
        file.write('\n---\n' + response)


# Основная функция для запуска программы
def run(target, num_requests):
    # Список выполненных команд
    commands = []
    for i in range(num_requests):
        print(f'- Request {i} -')
        prompts = get_prompts()
        # Добавление основной задачи в последний промпт
        prompts[-1]['content'] += f'\nMain goal: {target}\n-- End of header. Waiting for assistant reaction --'
        execution_result = get_code_result()
        
        # Если список выполненных команд не пуст, то последняя команда добавляется в промпт
        if commands:
            prompts.append({'role': 'assistant', 
            'content': f'{commands[-1]["command"]} {commands[-1]["args"]}'})
        
        # Если была выполнена команда, добавляется результат ее выполнения в промпт
        current_file = current_block.split(':')[0]
        if execution_result:
            prompts.append({'role': 'user', 
            'content': f'"{current_file}" execution result: ```{execution_result}\n```'})
        # Добавление промпта для ожидания новой команды от пользователя
        prompts.append({'role': 'user', 
            'content': f'- Command executed. Waiting for a command from assistant - '})
        # Запись списка промптов в файл
        log_prompts(prompts)
        gpt_response = generate_message(prompts)
        log_gpt_response(gpt_response)
        commands = handle_text(gpt_response)
        if commands:
            execute_command(commands[-1]['command'])


# Основная функция программы
def main():
    remove_files()
    create_file('main.py')
    target = input('AI Target>> ')
    num_requests = int(input('Number of requests>> '))
    run(target, num_requests)


if __name__ == '__main__':
    main()