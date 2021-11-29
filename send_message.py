import aiofiles
import asyncio
import configargparse
import logging

import datetime


logger = logging.getLogger('__name__')


def parse():
    parser = configargparse.ArgumentParser(default_config_files=['./config.txt'])
    parser.add('--host', help='Chat host')
    parser.add('--port', help='Chat port')
    parser.add('--history', help='Where to save chat history')
    return parser


async def send_message(parser_args, message):
    reader, writer = await asyncio.open_connection(
        parser_args.host, 5050
    )

    account_hash = 'bc744a84-5161-11ec-8c47-0242ac110002'
    message_to_send = f'{account_hash}\n{message}\n\n'

    writer.write(message_to_send.encode())

    writer.close()


if __name__ == '__main__':
    parser_args = parse().parse_args()

    asyncio.run(send_message(parser_args, 'Message'))