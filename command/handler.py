"""
消息处理器
"""

import json
from .convert.processors import MessageProcessors
from ..robot.test.test_methods import test_process_demo
from config.setting import OBJECT
from robot.control.manager import judge_command as robot_command
from convert.processors import judge_command as blender_command

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
            data = json.loads(message)

            # 处理首次连接消息
            if 'username' in data and len(data) == 1:
                response = {
                    "type": "system",
                    "content": "注册成功",
                    "target": sender_username
                }
                await self.connected_clients[sender_username].send(json.dumps(response))
                return
                
            # 根据OBJECT类型处理消息
            if OBJECT in ["robot", "both"]:
                # 机器人控制逻辑
                await robot_command(data)
            
            if OBJECT in ["model", "both"]:
                # 转成blender命令
                if "blender" in self.connected_clients:
                    await blender_command(data)
                else:
                    print("Blender client not connected")
                
        except json.JSONDecodeError:
            print("Invalid JSON message")
        except Exception as e:
            print(f"Error processing message: {e}")