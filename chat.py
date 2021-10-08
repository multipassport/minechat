import asyncio


async def connect_to_chat():
    reader, writer = await asyncio.open_connection(
        'minechat.dvmn.org', 5000
    )
    while True:
        data = await reader.read(100)
        print(data.decode('utf-8'))


if __name__ == '__main__':
    asyncio.run(connect_to_chat())
