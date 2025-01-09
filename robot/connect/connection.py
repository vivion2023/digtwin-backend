"""
机器人连接
"""

from ..sdk import Auboi5Robot, logger_init, logger, RobotErrorType
import time

class RobotConnection:
    def __init__(self, ip='192.168.40.130', port=8899):
        self.ip = ip
        self.port = port
        self.robot = None
        
    def connect(self):
        # Initialize logger
        logger_init()
        logger.info(f"{Auboi5Robot.get_local_time()} connection beginning...")
        
        # Initialize system
        Auboi5Robot.initialize()
        
        # Create robot control instance
        self.robot = Auboi5Robot()
        
        # Create context
        handle = self.robot.create_context()
        logger.info(f"robot.rshd={handle}")
        
        try:
            # Connect to server
            result = self.robot.connect(self.ip, self.port)
            
            if result != RobotErrorType.RobotError_SUCC:
                logger.info(f"connect server {self.ip}:{self.port} failed.")
                return None
            
            return self.robot
            
        except Exception as e:
            logger.error(f"Robot Connection Error: {e}")
            self.disconnect()
            return None
            
    def disconnect(self):
        if self.robot and self.robot.connected:
            self.robot.robot_shutdown()
            self.robot.disconnect()
        Auboi5Robot.uninitialize()