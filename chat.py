import asyncio
import configargparse


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
        data = await reader.read(100)
        print(data.decode('utf-8'))


if __name__ == '__main__':
    parser_args = parse().parse_args()
    asyncio.run(connect_to_chat(parser_args))
