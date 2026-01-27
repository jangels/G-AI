from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal

# ========== 输入：统一的意图请求 ==========
class RawBeggingRequest(BaseModel):
    """
    统一的意图请求模型
    所有操作都抽象为"意图"，通过 intent_type 和 action 来区分
    """
    # 核心意图描述（自然语言）
    user_intent: str = Field(..., title="用户意图", example="我想买个便宜的二手 iPhone 13")
    
    # 意图类型（模块）
    intent_type: Literal[
        "goods",      # 丐物 - 商品需求
        "codes",      # 丐码 - 数字资产
        "knowledge",   # 丐知 - 知识悬赏
        "companions", # 丐伴 - AI伴侣
        "prompts",    # 丐咒 - Prompt市场
        "console",    # 丐帮 - 控制台
        "copy"        # 纯文案生成（默认）
    ] = Field("copy", title="意图类型/模块")
    
    # 操作类型
    action: Literal[
        "list",      # 查询列表
        "get",       # 获取详情
        "create",    # 创建
        "update",    # 更新
        "delete",    # 删除
        "join",      # 加入（goods专用）
        "rent",      # 租用（codes专用）
        "claim",     # 认领（knowledge专用）
        "solve",     # 解决（knowledge专用）
        "purchase",  # 购买（prompts专用）
        "stats",     # 统计（console专用）
        "logs",      # 日志（console专用）
        "generate"   # 生成文案（copy专用，默认）
    ] = Field("generate", title="操作类型")
    
    # 业务数据（可选，根据 action 不同而不同）
    data: Optional[Dict[str, Any]] = Field(None, title="业务数据", example={
        "id": 1,
        "item_name": "iPhone 13",
        "target_price": 2000
    })
    
    # 查询参数（用于 list/get 操作）
    filters: Optional[Dict[str, Any]] = Field(None, title="查询筛选", example={
        "status": "active",
        "search": "iPhone"
    })
    
    # 其他元数据
    budget: Optional[str] = Field(None, title="预算")
    platform: Optional[str] = Field("WECHAT", title="分发平台")

# ========== 输出：统一的意图响应 ==========
class IntentResponse(BaseModel):
    """
    统一的意图响应模型
    根据不同的 intent_type 和 action，返回不同的数据结构
    """
    success: bool = Field(..., title="是否成功")
    intent_type: str = Field(..., title="意图类型")
    action: str = Field(..., title="执行的操作")
    
    # 响应数据（根据操作类型动态变化）
    data: Optional[Any] = Field(None, title="响应数据")
    
    # 文案生成结果（如果是 copy 类型）
    copy: Optional[Dict[str, Any]] = Field(None, title="生成的文案", example={
        "style": "CYBER_MISERABLE",
        "content": "检测到碳基生物对...",
        "hashtags": ["#CyberBegging"],
        "skill_confidence": 0.98
    })
    
    # 错误信息
    error: Optional[str] = Field(None, title="错误信息")
    
    # 元数据
    message: Optional[str] = Field(None, title="提示信息")
    timestamp: Optional[str] = Field(None, title="时间戳")