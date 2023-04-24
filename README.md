# Скрипт для генерации кода с помощью GPT-3.5

Данный проект представляет собой интеллектуального помощника для работы с кодом. Он позволяет легко навигировать по проекту, добавлять и редактировать код, создавать задачи и выполнять их. Программа использует искусственный интеллект GPT-3.5 для генерации текста и выполнения команд.

## Установка и запуск

Для установки необходимо склонировать репозиторий:

```
git clone https://github.com/RuslanKoroy/gpt-codewriter
```

Для работы программы необходим Python 3.7 или выше. Установите все необходимые зависимости, используя команду:

```
pip install -r requirements.txt
```

Для запуска программы выполните команду:

```
python main.py
```

## Использование

После запуска программы укажите цель и количество запросов, которые выполнит GPT-3.5. Программа использует искусственный интеллект GPT-3.5 для генерации текста и выполнения команд. Чтобы использовать GPT-3.5, необходимо зарегистрироваться на сайте OpenAI и получить ключи API. 

После этого необходимо в файле constants.py изменить переменную openai_api_keys на соответствующие значения. Можно использовать несколько ключей с разных аккаунтов, чтобы избежать ограничения в 3 генерации в минуту.

Данные о работе программы записываются в несколько файлов, которые находятся в папке scripts проекта. Файл notes.json содержит заметки и задачи, которые пользователь может создавать в рамках работы с программой. 

Файл block_list.md содержит список всех блоков кода, которые были обработаны программой. Файл descriptions.json содержит описания блоков кода. Функция check_block_descriptions() проверяет, есть ли описание для каждого блока в списке block_list, и если его нет, вызывает функцию describe_block(), которая запрашивает у GPT описание блока и записывает его в descriptions.json.