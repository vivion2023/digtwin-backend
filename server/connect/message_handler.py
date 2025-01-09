"""
消息处理器
"""

import json
from command.convert.processors import MessageProcessors
from robot.connect.connection import RobotConnection
from robot.control.control_method import test_process_demo

class MessageHandler:
    def __init__(self, connected_clients):
        """
        初始化消息处理器
        Args:
            connected_clients: 存储所有websocket连接的字典 {username: websocket}
        """
        self.connected_clients = connected_clients
        self.processors = MessageProcessors()

    async def handle_message(self, message: str, sender_username: str):
        """
        处理接收到的消息
        Args:
            message: 接收到的消息字符串
            sender_username: 发送消息的用户名
        """
        try:
            # 处理首次连接消息
            data = json.loads(message)
            if 'username' in data and len(data) == 1:
                response = {
                    "type": "system",
                    "content": "注册成功",
                    "target": sender_username
                }
                await self.connected_clients[sender_username].send(json.dumps(response))
                return
                
            # 获取目标用户名
            target = await self.processors.get_target(data)
            # 处理消息，移除target字段
            message = await self.processors.process_message(data)
            
            # 发送消息给目标连接
            if target in self.connected_clients:
                await self.connected_clients[target].send(json.dumps(data))
            else:
                # 如果目标用户不存在，则测试机器人控制
                # 建立连接
                robot_connection = RobotConnection()
                robot = robot_connection.connect()
                if robot:  # 确保连接成功
                    try:
                        # 初始化机器人
                        # 测试机器人控制
                        test_process_demo()
                    finally:
                        # 确保最后断开连接
                        robot_connection.disconnect()

                print(f"Target {target} not found in connected clients")
                
        except json.JSONDecodeError:
            print("Invalid JSON message")
        except Exception as e:
            print(f"Error processing message: {e}")