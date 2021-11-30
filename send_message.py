import asyncio
import json
import logging

import configargparse

logger = logging.getLogger('__name__')


def parse():
    parser = configargparse.ArgumentParser(default_config_files=['./sender_config.txt'])
    parser.add('--host', help='Chat host')
    parser.add('--port', help='Chat port')
    parser.add('--history', help='Where to save chat history')
    parser.add('--account_hash', help='Account hash to login')
    parser.add('message', help='Message to send')
    parser.add('--nickname', help='Preffered nickname')
    return parser


async def register(reader, writer, parser_args):
    server_reply = await reader.readline()
    logging.debug(server_reply)

    escaped_nickname = fr'{parser_args.nickname}'

    logging.debug(f'Registering {escaped_nickname}')
    message_to_register = f'\n{escaped_nickname}\n'
    writer.write(message_to_register.encode())

    server_reply = await reader.readline()
    logging.debug(server_reply)
    server_reply = await reader.readline()
    logging.debug(server_reply)

    account_hash = json.loads(server_reply)['account_hash']
    with open('sender_config.txt', 'a', encoding='utf-8') as file:
        file.write(f'\naccount_hash={account_hash}')
    logging.debug('Registered a new user')


async def authorize(reader, writer, parser_args):
    logging.debug('Authorizing')
    message_to_send = f'{parser_args.account_hash}\n'

    server_reply = await reader.readline()
    logging.debug(server_reply.decode())

    writer.write(message_to_send.encode())


async def send_message(reader, writer, parser_args, account_hash):
    escaped_message = fr'{parser_args.message}'
    logging.debug(f'Sending message: \n\t{escaped_message}')

    message_to_send = f'{escaped_message}\n\n'

    server_reply_json = await reader.readline()
    logging.debug(server_reply_json.decode())

    if not json.loads(server_reply_json):
        print('Неизвестный токен. Проверьте его или зарегистрируйте заново.')
        logging.error('Incorrect token')

    writer.write(message_to_send.encode())

    server_reply = await reader.readline()
    logging.debug(server_reply.decode())


async def chat(parser_args):
    reader, writer = await asyncio.open_connection(
        parser_args.host, parser_args.port,
    )

    if not (account_hash := parser_args.account_hash):
        account_hash = await register(reader, writer, parser_args)

    await authorize(reader, writer, parser_args)
    await send_message(reader, writer, parser_args, account_hash)

    writer.close()


if __name__ == '__main__':
    parser_args = parse().parse_args()

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG,
        filename='chatlog.log',
    )

    asyncio.run(chat(parser_args))
