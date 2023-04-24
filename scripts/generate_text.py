import openai
import tiktoken
from time import sleep
from constants import openai_api_keys, gpt_model
from itertools import cycle


api_keys = cycle(openai_api_keys)


# Определяем функцию для подсчета количества токенов в тексте
def get_token_count(text):
    encoding = tiktoken.encoding_for_model(gpt_model)
    return len(encoding.encode(text))

# Определяем функцию для разбиения списка промптов на более короткие, если их общее количество токенов превышает максимально допустимое значение
def cut_prompts(prompts, prompts_len=4, max_len=3800):
    text = ''.join([prompt['content'] for prompt in prompts])
    token_count = get_token_count(text)
    while token_count > max_len:
        prompts = prompts[:prompts_len] + prompts[prompts_len + 1:]
        text = ''.join([prompt['content'] for prompt in prompts])
        token_count = get_token_count(text)
    return prompts

# Определяем функцию для отправки запроса к API, повторяющую запросы при возникновении ошибок
def try_until(prompts):
    for _ in range(5):
        try:
            message = api_request(prompts)
            sleep(5)
            return message
        except Exception as exception:
            print(f'Ошибка в try_until: {exception}')
            sleep(20)
    return ''

# Определяем функцию для получения списка промптов из файла
def get_prompt():
    with open('prompt_short_en.md', encoding='utf-8') as file:
        text = ''.join(file.readlines())
    text = text.split('$')
    return text

# Определяем функцию для отправки запроса к API
def api_request(prompts):
    openai.api_key = next(api_keys)
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompts
    )
    message = completion['choices'][0]['message']['content']
    return message

# Определяем функцию для генерации сообщения на основе списка промптов
def generate_message(prompts, prompts_len=4):
    #prompts = cut_prompts(prompts, prompts_len=prompts_len)
    message = try_until(prompts)
    return message

