#!/usr/bin/env python

import asyncio
import json
import uuid
from typing import Dict

import websockets

# 存储所有websocket连接的字典
# key: session_id, value: websocket connection
connected_clients: Dict[str, websockets.WebSocketServerProtocol] = {}


async def register_client(websocket) -> str:
    """注册新的websocket返回session_id客户端"""
    session_id = str(uuid.uuid4())
    connected_clients[session_id] = websocket
    print(f"New client connected. Session ID: {session_id}. Total clients: {len(connected_clients)}")
    return session_id


async def unregister_client(session_id):
    """注销websocket客户端"""
    if session_id in connected_clients:
        del connected_clients[session_id]
        print(f"Client {session_id} disconnected. Total clients: {len(connected_clients)}")


async def send_message(websocket, message):
    """发送消息给websocket客户端"""
    await websocket.send(json.dumps(message))


async def handler(websocket):
    """处理websocket连接"""
    session_id = await register_client(websocket)

    try:
        # 发送session_id给客户端
        await send_message(websocket, {
            "type": "session_id",
            "session_id": session_id
        })
        
        while True:
            try:
                await websocket.recv()
            except websockets.exceptions.ConnectionClosedOK:
                print("Closed connection.")
                break
            except websockets.exceptions.ConnectionClosedError:
                print("Closed connection.")
                break

    finally:
        await unregister_client(session_id)


async def start_server():
    """启动websocket服务器"""
    print("Starting backend server. Waiting for websocket messages... (Press Ctrl + C to quit)")
    async with websockets.serve(handler, "", 5001):
        await asyncio.Future()  # run forever
