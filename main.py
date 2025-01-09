import asyncio
from websocket.manager import start_server
from command.handler import MessageHandler

async def main():
    # 启动websocket服务器
    await start_server()

if __name__ == '__main__':
    asyncio.run(main())
    # test_process_demo()