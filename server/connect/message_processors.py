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
    
    