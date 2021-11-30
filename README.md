# Minecraft Chat

На данный момент проект состоит из двух скриптов, соединяющийся с чатом посредством asyncio. `read_chat.py` выводит чат в консоль, а также ведет историю переписки в текстовый файл. `send_message.py` отправляет сообщение в чат.

## Конфигурация

Конфигурация скриптов представлена в файлах `sender_config.txt` и `reader_config.txt` для каждого из скриптов соответсвенно. После первого запуска `send_message.py` туда также добавляется настройка account_hash, которая будет использована для последующей авторизации текущего пользователя.
Кроме того, можно использовать аргументы командной строки, которые имеют более высокий приоритет, чем настройки из файлов конфигурации.

## Аргументы командной строки

Аргументы командной строки можно просмотреть командами

```bash
python read_chat.py --help
```

```bash
python send_message.py --help
```

* `--host` - адрес чата
* `--port` - порт чата
* `--history` - желаемое место для сохранения история переписки в чате
* `--nickname` - ник в чате
* `--account_hash` - хэш аккаунта, используемый при авторизации. Получается автоматически при первом запуски `send_message.py`

## Запуск

При условии заполненных конфигов скрипты запускаются следующими командами

```bash
python read_chat.py
```

```bash
python send_message.py MESSAGE
```

где `MESSAGE` - сообщение для отправки в чат

## Цели проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
