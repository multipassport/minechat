import asyncio
import json
import logging

import aiofiles
import configargparse

logger = logging.getLogger(__name__)


def parse_cli_args():
    parser = configargparse.ArgumentParser(default_config_files=['./sender_config.txt'])
    parser.add('--host', help='Chat host')
    parser.add('--port', help='Chat port')
    parser.add('--account_hash', help='Account hash to login')
    parser.add('message', help='Message to send')
    parser.add('--nickname', help='Preffered nickname')
    return parser


async def register(parser_args, nickname):
    reader, writer = await asyncio.open_connection(
        parser_args.host, parser_args.port,
    )
    server_reply = await reader.readline()
    logging.debug(server_reply)

    escaped_nickname = fr'{nickname}'

    logging.debug(f'Registering {escaped_nickname}')
    message_to_register = f'\n{escaped_nickname}\n'
    writer.write(message_to_register.encode())
    await writer.drain()

    server_reply = await reader.readline()
    logging.debug(server_reply)
    server_reply = await reader.readline()
    logging.debug(server_reply)

    account_hash = json.loads(server_reply)['account_hash']
    async with aiofiles.open('sender_config.txt', 'a', encoding='utf-8') as file:
        await file.write(f'\naccount_hash={account_hash}')
    logging.debug('Registered a new user')

    writer.close()

    return account_hash


async def authorize(reader, writer, account_hash):
    logging.debug('Authorizing')
    message_to_send = f'{account_hash}\n'

    server_reply = await reader.readline()
    logging.debug(server_reply.decode())

    writer.write(message_to_send.encode())
    await writer.drain()

    server_reply_json = await reader.readline()
    logging.debug(server_reply_json.decode())

    if not json.loads(server_reply_json):
        print('Неизвестный токен. Проверьте его или зарегистрируйте заново.')
        logging.error('Incorrect token')


async def send_message(reader, writer, message, account_hash):
    escaped_message = fr'{message}'
    logging.debug(f'Sending message: \n\t{escaped_message}')

    message_to_send = f'{escaped_message}\n\n'

    writer.write(message_to_send.encode())
    await writer.drain()

    server_reply = await reader.readline()
    logging.debug(server_reply.decode())


async def chat(parser_args):
    reader, writer = await asyncio.open_connection(
        parser_args.host, parser_args.port,
    )

    if not (account_hash := parser_args.account_hash):
        account_hash = await register(parser_args, parser_args.nickname)

    await authorize(reader, writer, account_hash)
    await send_message(reader, writer, parser_args.message, account_hash)

    writer.close()


if __name__ == '__main__':
    parser_args = parse_cli_args().parse_args()

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG,
        filename='send_message.log',
    )

    asyncio.run(chat(parser_args))
