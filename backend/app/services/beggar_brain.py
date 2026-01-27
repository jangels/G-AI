"""
Beggar-X: The Core Transformation Engine
统一的意图处理引擎 - 所有操作都抽象为意图
"""
from app.models.schemas import RawBeggingRequest, IntentResponse
from app.services.intent_router import IntentRouter

class BeggarBrain:
    """
    Beggar-X: The Core Transformation Engine
    统一的意图处理引擎 - 所有需求都抽象为意图
    """
    
    def __init__(self):
        self.router = IntentRouter()
    
    async def process_intent(self, request: RawBeggingRequest) -> IntentResponse:
        """
        处理意图 - 统一入口
        根据 intent_type 和 action 路由到对应的处理器
        """
        print(f"🧠 G-AI CORTEX: Processing intent -> [{request.intent_type}.{request.action}] {request.user_intent}")
        
        try:
            result = await self.router.route(request)
            result.timestamp = __import__('datetime').datetime.now().isoformat()
            return result
        except Exception as e:
            return IntentResponse(
                success=False,
                intent_type=request.intent_type,
                action=request.action,
                error=f"Neural Link Severed: {str(e)}",
                timestamp=__import__('datetime').datetime.now().isoformat()
            )

brain_instance = BeggarBrain()