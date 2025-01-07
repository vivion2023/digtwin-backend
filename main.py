import asyncio
from server.robot_control.test_methods import test_process_demo
from server.connect.websocker_server_connect import start_server
from server.robot_control.test_methods import test_process_demo

async def main():
    # 启动websocket服务器
    await start_server()

if __name__ == '__main__':
    asyncio.run(main())
    # test_process_demo()