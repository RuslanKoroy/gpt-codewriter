from scripts.generate_text import generate_message


# функция, которая генерирует краткое описание содержания файла по его пути
def describe_file(filepath):
    with open(filepath, 'r', encoding='utf8') as f:
        text = f.read()
    prompt = {'role': 'user', 
    'content': f'Briefly describe this text (up to 100 characters):\n"""\n{text}\n"""'}
    description = generate_message([prompt])
    return description


def describe(text):
    prompt = {'role': 'user', 
    'content': f'Briefly describe this text (up to 100 characters):\n"""\n{text}\n"""'}
    description = generate_message([prompt])
    return description


def summarize(text):
    with open(filepath, 'r', encoding='utf8') as f:
        text = f.read()
    prompt = {'role': 'user', 
    'content': f'Summarize this text (up to 100 characters):\n"""\n{text}\n"""'}
    description = generate_message([prompt])
    return summary


def explain_text(text):
    with open(filepath, 'r', encoding='utf8') as f:
        text = f.read()
    prompt = {'role': 'user', 
    'content': f'Briefly explain this (up to 100 characters):\n"""\n{text}\n"""'}
    description = generate_message([prompt])
    return description
