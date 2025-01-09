from config.robot import JOINT_MAX_VELOCITY, JOINT_MAX_ACC, COLLISION_LEVEL, ARRIVAL_AHEAD_BLEND
import time
from math import pi

def init_params(robot):
    """应用机器人初始化参数"""
    # 初始化运动属性
    robot.init_profile()
    
    # 设置关节最大速度和加速度
    robot.set_joint_maxvelc(JOINT_MAX_VELOCITY)
    robot.set_joint_maxacc(JOINT_MAX_ACC)
    
    # 设置碰撞等级
    robot.set_collision_class(COLLISION_LEVEL)
    
    # 设置到位前瞻量
    robot.set_arrival_ahead_blend(ARRIVAL_AHEAD_BLEND)

def demo_path(robot):
    """执行演示运动路径"""

    joint_radian = (0.541678, 0.225068, -0.948709, 0.397018, -1.570800, 0.541673)
    robot.move_joint(joint_radian, True)
    

    joint_radian = (55.5/180.0*pi, -20.5/180.0*pi, -72.5/180.0*pi, 38.5/180.0*pi, -90.5/180.0*pi, 55.5/180.0*pi)
    robot.move_joint(joint_radian, True)

    joint_radian = (0, 0, 0, 0, 0, 0)
    robot.move_joint(joint_radian, True)

    print("-----------------------------")
