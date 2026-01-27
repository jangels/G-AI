from fastapi import APIRouter, HTTPException
from app.models.schemas import RawBeggingRequest, IntentResponse
from app.services.beggar_brain import brain_instance

router = APIRouter()

@router.post("/beg", response_model=IntentResponse)
async def process_intent(request: RawBeggingRequest):
    """
    [Universal Endpoint] 统一的意图处理接口
    
    所有操作都抽象为"意图"，通过以下参数区分：
    - intent_type: 意图类型（goods/codes/knowledge/companions/prompts/console/copy）
    - action: 操作类型（list/get/create/update/delete/join/rent/claim/solve/purchase/generate）
    - user_intent: 自然语言描述的用户意图
    - data: 业务数据（可选）
    - filters: 查询筛选（可选）
    
    示例请求：
    ```json
    {
        "user_intent": "我想查看所有商品需求",
        "intent_type": "goods",
        "action": "list",
        "filters": {"status": "active"}
    }
    ```
    
    ```json
    {
        "user_intent": "我想买个便宜的iPhone",
        "intent_type": "copy",
        "action": "generate",
        "budget": "2000元"
    }
    ```
    """
    try:
        result = await brain_instance.process_intent(request)
        if not result.success:
            raise HTTPException(status_code=400, detail=result.error or "处理失败")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Neural Link Severed: {str(e)}")

@router.get("/health")
async def health_check():
    return {"status": "ONLINE", "philosophy": "SKILL_IS_BEGGING"}