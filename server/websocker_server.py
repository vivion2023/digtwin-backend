#!/usr/bin/env python

import asyncio
import json
import os
import uuid
from datetime import datetime
from typing import List, Tuple, Dict

import numpy as np
import websockets

try:
    width = os.get_terminal_size().columns
except:
    width = 20

# 存储所有websocket连接的字典
# key: session_id, value: websocket connection
connected_clients: Dict[str, websockets.WebSocketServerProtocol] = {}


async def register_client(websocket) -> str:
    """注册新的websocket返回session_id客户端，"""
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
    await websocket.send(json.dumps(message))


async def forward_message(sender_id: str, target_id: str, message: dict):
    """转发消息给指定的客户端"""
    if target_id in connected_clients:
        message["sender_id"] = sender_id
        await send_message(connected_clients[target_id], message)
        return True
    return False


async def handle_exception(websocket, error_message, status="ERROR"):
    print("Error:", error_message)
    message = {
        "status": status,
        "message": error_message
    }
    await websocket.send(json.dumps(message))


async def handler(websocket):
    session_id = await register_client(websocket)

    try:
        # 发送session_id给客户端
        await send_message(websocket, {
            "type": "session_id",
            "session_id": session_id
        })

        while True:
            try:
                message = await websocket.recv()
            except websockets.exceptions.ConnectionClosedOK:
                print("Closed connection.")
                break
            except websockets.exceptions.ConnectionClosedError:
                print("Closed connection.")
                break

            print("=" * width)
            print("Received websocket message.")
            print(message)

            try:
                data = json.loads(message)

                if "action" in data:
                    action = data["action"]

                    if action == 0:
                        print("Handling request (random number)")
                        x = np.random.rand()
                        y = np.random.rand()
                        z = np.random.rand()
                        await send_message(websocket, {'action': action, 'x': x, 'y': y, 'z': z})
                    elif action == 1:
                        print(message)

                # 处理转发消息
                if "target" in data and "content" in data:
                    target_id = data["target"]
                    success = await forward_message(
                        session_id,
                        target_id,
                        {"content": data["content"]}
                    )
                    if not success:
                        await handle_exception(
                            websocket,
                            f"Target client {target_id} not found"
                        )

            except Exception as e:
                print("Malformed input message:", e)
                continue

    finally:
        # 确保在连接关闭时注销客户端
        await unregister_client(session_id)


async def main():
    print("Starting backend server. Waiting for websocket messages... (Press Ctrl + C to quit)")
    async with websockets.serve(handler, "", 5001):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
