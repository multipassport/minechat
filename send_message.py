import aiofiles
import asyncio
import configargparse
import logging

import datetime


logger = logging.getLogger('__name__')


def parse():
    parser = configargparse.ArgumentParser(default_config_files=['./sender_config.txt'])
    parser.add('--host', help='Chat host')
    parser.add('--port', help='Chat port')
    parser.add('--history', help='Where to save chat history')
    parser.add('message', help='Message to send')
    return parser


async def send_message(parser_args):
    reader, writer = await asyncio.open_connection(
        parser_args.host, parser_args.port,
    )

    account_hash = 'bc744a84-5161-11ec-8c47-0242ac110002'
    message_to_send = f'{account_hash}\n{parser_args.message}\n\n'
    print(message_to_send)

    server_reply = await reader.readline()
    print(server_reply.decode())
    logging.info(server_reply.decode())

    writer.write(message_to_send.encode())

    server_reply_json = await reader.readline()
    print(server_reply_json.decode())
    logging.info(server_reply_json.decode())

    writer.close()


if __name__ == '__main__':
    parser_args = parse().parse_args()

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        filename='chatlog.log',
    )

    asyncio.run(send_message(parser_args))