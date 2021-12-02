import aiofiles
import asyncio
import configargparse
import logging

import datetime


logger = logging.getLogger(__name__)


def parse_cli_args():
    parser = configargparse.ArgumentParser(default_config_files=['./reader_config.txt'])
    parser.add('--host', help='Chat host')
    parser.add('--port', help='Chat port')
    parser.add('--history', help='Where to save chat history')
    return parser


async def connect_to_chat(chat_host, chat_port, history_location):
    logging.debug('Connecting to chat')

    reader, writer = await asyncio.open_connection(
        chat_host, chat_port,
    )

    while True:
        chat_message = await reader.readline()
        message_time = datetime.datetime.now().strftime('%d.%m.%y %H:%M')
        decoded_message = chat_message.decode()
        message_with_timestamp = f'[{message_time}] {decoded_message}'

        async with aiofiles.open(history_location, mode='a', encoding='utf-8') as file:
            await file.writelines(message_with_timestamp)

        print(message_with_timestamp)


if __name__ == '__main__':
    parser_args = parse_cli_args().parse_args()

    chat_host = parser_args.host
    chat_port = parser_args.port
    history_location = parser_args.history

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        filename='read_chat.log',
    )

    asyncio.run(connect_to_chat(chat_host, chat_port, history_location))
