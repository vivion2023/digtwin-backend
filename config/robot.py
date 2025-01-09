# robot_config.py
IP = '192.168.40.130'
PORT = 8899
LOG_PATH = './logfiles'

# 关节最大速度 (单位: rad/s)
JOINT_MAX_VELOCITY = (2.596177, 2.596177, 2.596177, 3.110177, 3.110177, 3.110177)

# 关节最大加速度 (单位: rad/s²)
# 原始最大加速度除以2.5作为实际使用值
JOINT_MAX_ACC = tuple(17.308779/2.5 for _ in range(6))

# 碰撞等级 (范围: 0-10)
COLLISION_LEVEL = 7

# 到位前瞻量 (单位: 米)
ARRIVAL_AHEAD_BLEND = 0.05

# 初始关节角度 (单位: 弧度)
INIT_JOINT_POSITIONS = (0, 0, 0, 0, 0, 0)