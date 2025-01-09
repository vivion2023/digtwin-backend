"""
机器人连接-异步
"""

import sys
import os
import asyncio
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from robot.sdk import Auboi5Robot, logger_init, logger, RobotErrorType
from config.robot import IP, PORT, LOG_PATH
import time
from robot.control.control_method import init_params, demo_path

class RobotConnection:
    def __init__(self, ip=IP, port=PORT):
        # 初始化机器人IP地址和端口
        self.ip = ip
        self.port = port
        self.robot = None
        self._running = False
        
    async def connect(self):
        # 初始化日志系统
        logger_init()
        logger.info(f"{Auboi5Robot.get_local_time()} connection beginning...")
        
        # 初始化机器人系统
        Auboi5Robot.initialize()
        
        # 创建机器人控制实例
        self.robot = Auboi5Robot()
        
        # 创建上下文
        handle = self.robot.create_context()
        logger.info(f"robot.rshd={handle}")
        
        try:
            # 连接到服务器
            result = self.robot.connect(self.ip, self.port)
            
            if result != RobotErrorType.RobotError_SUCC:
                logger.info(f"connect server {self.ip}:{self.port} failed.")
                return None
            
            # 启用事件系统
            self.robot.enable_robot_event()
            self.robot.init_profile()
            
            # 应用初始化参数
            init_params(self.robot)

            self._running = True
            return self.robot
            
        except Exception as e:
            logger.error(f"Robot Connection Error: {e}")
            self.disconnect()
            return None
            
    async def disconnect(self):
        # 断开连接并清理资源
        self._running = False
        if self.robot and self.robot.connected:
            self.robot.robot_shutdown()
            self.robot.disconnect()
            logger.info("disconnect server success.")
        Auboi5Robot.uninitialize()

async def main():
    # 创建连接实例
    robot_conn = RobotConnection()
    
    try:
        # 建立连接
        robot = await robot_conn.connect()
        if robot:
            logger.info(f"connect server {robot_conn.ip}:{robot_conn.port} success.")

            try:
                # 测试执行演示路径
                for i in range(3):
                    demo_path(robot)
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("receive exit signal")

    except Exception as e:
        logger.error(f"run error: {e}")
    finally:
        # 确保正常断开连接
        await robot_conn.disconnect()
        logger.info("program exit.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("program exit.")