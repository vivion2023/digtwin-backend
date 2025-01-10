"""
消息处理方法
"""

async def judge_command(message):
    """处理blender命令"""
    if message["command"] == "init_bones":
        print("init_bones")
        
async def init_bones(message):
    """初始化机器人骨骼"""
    print("init_bones")
    
class MessageProcessors:
    
    async def get_target(self, message_data: dict) -> str:
        """从消息中提取target字段"""
        target = message_data.get('target')
        if not target:
            raise ValueError("Message missing 'target' field")
        return target
    
    async def process_message(self, message_data: dict) -> dict:
        """处理消息，移除target字段"""
        message_data.pop('target', None)
        return message_data
    
    