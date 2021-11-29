import aiofiles
import asyncio
import configargparse
import logging

import datetime


logger = logging.getLogger(__name__)


def parse():
    parser = configargparse.ArgumentParser(default_config_files=['./config.txt'])
    parser.add('--host', help='Chat host')
    parser.add('--port', help='Chat port')
    parser.add('--history', help='Where to save chat history')
    return parser


async def connect_to_chat(parser_args):
    reader, writer = await asyncio.open_connection(
        parser_args.host, parser_args.port,
    )
    while True:
        chat_message = await reader.readline()
        message_time = datetime.datetime.now().strftime('%d.%m.%y %H:%M')
        decoded_message = chat_message.decode()
        message_with_timestamp = f'[{message_time}] {decoded_message}'

        async with aiofiles.open(parser_args.history, mode='a', encoding='utf-8') as file:
            await file.writelines(message_with_timestamp)

        print(message_with_timestamp)


if __name__ == '__main__':
    parser_args = parse().parse_args()
    # print(datetime.datetime.now().strftime('%d.%m.%y %H:%M'))
    # print(datetime.datetime.now().strftime())

    logging.basicConfig(
        format='%(asctime)s - %(message)s',
        level=logging.INFO,
        # filename=parser_args.history,
    )
    asyncio.run(connect_to_chat(parser_args))
