from config.robot import JOINT_MAX_VELOCITY, JOINT_MAX_ACC, COLLISION_LEVEL, ARRIVAL_AHEAD_BLEND
import time
from math import pi

async def judge_command(message):
    """处理机器人命令"""
    if message["command"] == "init_bones":
        init_bones()
    elif message["command"] == "start_posture":
        start_posture()
    elif message["command"] == "rotate_bones":
        angle = message["angle"]
        rotate_bones(angle)
    elif message["command"] == "end_program":
        end_program()
        

def init_bones(robot):
    """初始化机器人骨骼"""
    joint_radian = (0, 0, 0, 0, 0, 0)
    robot.move_joint(joint_radian, True)

def start_posture(robot):
    """开始姿态"""

def rotate_bones(robot, angle):
    """旋转机器人骨骼"""

def end_program(robot):
    """结束程序"""

def demo_path(robot):
    """执行演示运动路径"""

    joint_radian = (0.541678, 0.225068, -0.948709, 0.397018, -1.570800, 0.541673)
    robot.move_joint(joint_radian, True)
    

    joint_radian = (55.5/180.0*pi, -20.5/180.0*pi, -72.5/180.0*pi, 38.5/180.0*pi, -90.5/180.0*pi, 55.5/180.0*pi)
    robot.move_joint(joint_radian, True)

    joint_radian = (0, 0, 0, 0, 0, 0)
    robot.move_joint(joint_radian, True)

    print("-----------------------------")
