#!/usr/bin/env python

"""
websocket服务器
"""

import asyncio
import json
from typing import Dict
import websockets
from .message_handler import MessageHandler

# 存储所有websocket连接的字典
connected_clients: Dict[str, websockets.WebSocketServerProtocol] = {}

async def register_client(websocket, username: str) -> str:
    """注册新的websocket连接"""
    # 检查用户是否已经连接
    if username in connected_clients:
        print(f"Connection already exists for user: {username}")
        return None

    # 注册新连接
    connected_clients[username] = websocket
    print(f"New client connected. User: {username}")
    return username

async def unregister_client(username):
    """注销websocket客户端"""
    if username in connected_clients:
        del connected_clients[username]
        print(f"Client disconnected. User: {username}")

async def handler(websocket):
    """处理websocket连接"""
    username = None
    message_handler = MessageHandler(connected_clients)

    try:
        # 等待首次消息获取用户名
        first_message = await websocket.recv()
        try:
            data = json.loads(first_message)
            username = data.get('username')
            if not username:
                print("First message missing username field")
                return
            
            username = await register_client(websocket, username)
            if not username:
                return
                
        except json.JSONDecodeError:
            print("Invalid JSON in first message")
            return
        
        # 继续处理后续消息
        while True:
            try:
                message = await websocket.recv()
                await message_handler.handle_message(message, username)
            except websockets.exceptions.ConnectionClosedOK:
                print(f"Closed connection normally for {username}")
                break
            except websockets.exceptions.ConnectionClosedError:
                print(f"Closed connection with error for {username}")
                break

    finally:
        if username:
            await unregister_client(username)

async def start_server():
    """启动websocket服务器"""
    print("Starting backend server. Waiting for websocket messages... (Press Ctrl + C to quit)")
    async with websockets.serve(handler, "", 5001):
        await asyncio.Future()  # run forever
