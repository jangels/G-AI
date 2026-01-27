"""
意图路由器 - 根据意图类型和操作类型路由到不同的处理器
"""
from typing import Dict, Any
from app.models.schemas import RawBeggingRequest, IntentResponse
from datetime import datetime

# 简单的内存存储（生产环境应使用数据库）
_storage = {
    "goods": [],      # 商品需求
    "codes": [],      # 数字资产
    "knowledge": [],  # 知识悬赏
    "companions": [], # AI伴侣
    "prompts": [],    # Prompt市场
    "console": {      # 控制台数据
        "stats": {"total_requests": 8492, "gmv": 42109},
        "logs": []
    }
}

class IntentRouter:
    """意图路由器 - 统一处理所有意图"""
    
    async def route(self, request: RawBeggingRequest) -> IntentResponse:
        """根据意图类型和操作类型路由到对应的处理器"""
        
        intent_type = request.intent_type
        action = request.action
        
        # 路由表
        router_map = {
            "goods": self._handle_goods,
            "codes": self._handle_codes,
            "knowledge": self._handle_knowledge,
            "companions": self._handle_companions,
            "prompts": self._handle_prompts,
            "console": self._handle_console,
            "copy": self._handle_copy
        }
        
        handler = router_map.get(intent_type, self._handle_copy)
        return await handler(request)
    
    # ========== Goods (丐物) ==========
    async def _handle_goods(self, request: RawBeggingRequest) -> IntentResponse:
        action = request.action
        data = request.data or {}
        filters = request.filters or {}
        
        if action == "list":
            items = _storage["goods"]
            # 应用筛选
            if filters.get("status"):
                items = [i for i in items if i.get("status") == filters["status"]]
            return IntentResponse(
                success=True,
                intent_type="goods",
                action="list",
                data=items,
                message=f"找到 {len(items)} 个需求"
            )
        
        elif action == "get":
            item_id = data.get("id")
            items = _storage["goods"]
            item = next((i for i in items if i.get("id") == item_id), None)
            if not item:
                return IntentResponse(success=False, intent_type="goods", action="get", error="需求不存在")
            return IntentResponse(success=True, intent_type="goods", action="get", data=item)
        
        elif action == "create":
            new_id = len(_storage["goods"]) + 1
            new_item = {
                "id": new_id,
                "item_name": data.get("item_name", request.user_intent),
                "market_price": data.get("market_price", 0),
                "target_price": data.get("target_price", 0),
                "current_users": 0,
                "target_users": data.get("target_users", 100),
                "status": "PENDING",
                "created_at": datetime.now().isoformat()
            }
            _storage["goods"].append(new_item)
            return IntentResponse(
                success=True,
                intent_type="goods",
                action="create",
                data=new_item,
                message="需求创建成功"
            )
        
        elif action == "join":
            item_id = data.get("id")
            items = _storage["goods"]
            item = next((i for i in items if i.get("id") == item_id), None)
            if not item:
                return IntentResponse(success=False, intent_type="goods", action="join", error="需求不存在")
            item["current_users"] = item.get("current_users", 0) + 1
            if item["current_users"] >= item["target_users"]:
                item["status"] = "GATHERING"
            return IntentResponse(
                success=True,
                intent_type="goods",
                action="join",
                data=item,
                message="已加入需求"
            )
        
        return IntentResponse(success=False, intent_type="goods", action=action, error="不支持的操作")
    
    # ========== Codes (丐码) ==========
    async def _handle_codes(self, request: RawBeggingRequest) -> IntentResponse:
        action = request.action
        data = request.data or {}
        
        if action == "list":
            items = _storage["codes"]
            return IntentResponse(
                success=True,
                intent_type="codes",
                action="list",
                data=items,
                message=f"找到 {len(items)} 个资产"
            )
        
        elif action == "rent":
            asset_id = data.get("id")
            items = _storage["codes"]
            asset = next((i for i in items if i.get("id") == asset_id), None)
            if not asset:
                return IntentResponse(success=False, intent_type="codes", action="rent", error="资产不存在")
            # 模拟租用
            asset["status"] = "RENTED"
            return IntentResponse(
                success=True,
                intent_type="codes",
                action="rent",
                data=asset,
                message="租用成功"
            )
        
        return IntentResponse(success=False, intent_type="codes", action=action, error="不支持的操作")
    
    # ========== Knowledge (丐知) ==========
    async def _handle_knowledge(self, request: RawBeggingRequest) -> IntentResponse:
        action = request.action
        data = request.data or {}
        filters = request.filters or {}
        
        if action == "list":
            items = _storage["knowledge"]
            if filters.get("search"):
                search_term = filters["search"].lower()
                items = [i for i in items if search_term in i.get("title", "").lower() or search_term in i.get("description", "").lower()]
            return IntentResponse(
                success=True,
                intent_type="knowledge",
                action="list",
                data=items,
                message=f"找到 {len(items)} 个悬赏"
            )
        
        elif action == "create":
            new_id = len(_storage["knowledge"]) + 1
            new_item = {
                "id": new_id,
                "title": data.get("title", request.user_intent),
                "description": data.get("description", ""),
                "reward_amount": data.get("reward_amount", 0),
                "status": "OPEN",
                "created_at": datetime.now().isoformat()
            }
            _storage["knowledge"].append(new_item)
            return IntentResponse(
                success=True,
                intent_type="knowledge",
                action="create",
                data=new_item,
                message="悬赏创建成功"
            )
        
        elif action == "claim":
            bounty_id = data.get("id")
            items = _storage["knowledge"]
            item = next((i for i in items if i.get("id") == bounty_id), None)
            if not item:
                return IntentResponse(success=False, intent_type="knowledge", action="claim", error="悬赏不存在")
            return IntentResponse(
                success=True,
                intent_type="knowledge",
                action="claim",
                data=item,
                message="已认领悬赏"
            )
        
        return IntentResponse(success=False, intent_type="knowledge", action=action, error="不支持的操作")
    
    # ========== Companions (丐伴) ==========
    async def _handle_companions(self, request: RawBeggingRequest) -> IntentResponse:
        action = request.action
        data = request.data or {}
        
        if action == "list":
            items = _storage["companions"]
            return IntentResponse(
                success=True,
                intent_type="companions",
                action="list",
                data=items,
                message=f"找到 {len(items)} 个伴侣"
            )
        
        elif action == "create":
            new_id = len(_storage["companions"]) + 1
            new_item = {
                "id": new_id,
                "name": data.get("name", "Custom Companion"),
                "type": data.get("type", "Custom"),
                "rate_per_min": data.get("rate_per_min", 1.0),
                "status": "ONLINE",
                "created_at": datetime.now().isoformat()
            }
            _storage["companions"].append(new_item)
            return IntentResponse(
                success=True,
                intent_type="companions",
                action="create",
                data=new_item,
                message="伴侣创建成功"
            )
        
        return IntentResponse(success=False, intent_type="companions", action=action, error="不支持的操作")
    
    # ========== Prompts (丐咒) ==========
    async def _handle_prompts(self, request: RawBeggingRequest) -> IntentResponse:
        action = request.action
        data = request.data or {}
        filters = request.filters or {}
        
        if action == "list":
            items = _storage["prompts"]
            if filters.get("search"):
                search_term = filters["search"].lower()
                items = [i for i in items if search_term in i.get("title", "").lower()]
            return IntentResponse(
                success=True,
                intent_type="prompts",
                action="list",
                data=items,
                message=f"找到 {len(items)} 个Prompt"
            )
        
        elif action == "purchase":
            prompt_id = data.get("id")
            items = _storage["prompts"]
            item = next((i for i in items if i.get("id") == prompt_id), None)
            if not item:
                return IntentResponse(success=False, intent_type="prompts", action="purchase", error="Prompt不存在")
            return IntentResponse(
                success=True,
                intent_type="prompts",
                action="purchase",
                data=item,
                message="购买成功"
            )
        
        return IntentResponse(success=False, intent_type="prompts", action=action, error="不支持的操作")
    
    # ========== Console (丐帮) ==========
    async def _handle_console(self, request: RawBeggingRequest) -> IntentResponse:
        action = request.action
        
        if action == "stats":
            stats = _storage["console"]["stats"]
            return IntentResponse(
                success=True,
                intent_type="console",
                action="stats",
                data=stats
            )
        
        elif action == "logs":
            logs = _storage["console"]["logs"]
            return IntentResponse(
                success=True,
                intent_type="console",
                action="logs",
                data=logs
            )
        
        return IntentResponse(success=False, intent_type="console", action=action, error="不支持的操作")
    
    # ========== Copy (文案生成) ==========
    async def _handle_copy(self, request: RawBeggingRequest) -> IntentResponse:
        """生成乞讨文案（使用真实 LLM）"""
        from app.services.llm_service import llm_service
        
        try:
            # 调用真实的 LLM 服务
            copy_result = await llm_service.generate_begging_copy(
                user_intent=request.user_intent,
                budget=request.budget,
                platform=request.platform or "WECHAT"
            )
            
            return IntentResponse(
                success=True,
                intent_type="copy",
                action="generate",
                copy=copy_result,
                message="文案生成成功（由 Gemini AI 生成）"
            )
        except Exception as e:
            print(f"❌ 文案生成失败: {e}")
            # 降级到默认文案
            copy_result = {
                "style": "CYBER_MISERABLE (赛博卖惨)",
                "content": f"检测到碳基生物对 [{request.user_intent}] 的渴望，但其信用点储备不足（预算：{request.budget or '未知'}）。请求网络节点进行人道主义资源再分配。",
                "hashtags": ["#CyberBegging", "#LowBudgetDream", "#TechSalvation"],
                "skill_confidence": 0.75
            }
            return IntentResponse(
                success=True,
                intent_type="copy",
                action="generate",
                copy=copy_result,
                message="文案生成成功（降级模式）"
            )

# 初始化示例数据
def init_sample_data():
    """初始化示例数据"""
    _storage["goods"] = [
        {
            "id": 1,
            "item_name": "IPHONE 16 PRO (128G) - 丐版",
            "market_price": 7999,
            "target_price": 6500,
            "current_users": 842,
            "target_users": 1000,
            "status": "GATHERING",
            "created_at": datetime.now().isoformat()
        }
    ]
    
    _storage["codes"] = [
        {
            "id": 1,
            "asset_id": "0xAA_NETFLIX_4K",
            "asset_type": "STREAMING_ACC",
            "rate_per_hour": 0.5,
            "status": "AVAILABLE"
        }
    ]
    
    _storage["knowledge"] = [
        {
            "id": 1,
            "title": "如何在 Rust 中优化 WebAssembly 的内存碎片问题？",
            "description": "Context: 目前在处理 2GB+ 大文件上传时，WASM 内存占用飙升。",
            "reward_amount": 200.0,
            "status": "OPEN",
            "created_at": datetime.now().isoformat()
        }
    ]
    
    _storage["companions"] = [
        {
            "id": 1,
            "name": "EVA-01",
            "type": "LLM-Audio",
            "rate_per_min": 0.5,
            "status": "ONLINE"
        }
    ]
    
    _storage["prompts"] = [
        {
            "id": 1,
            "title": "霓虹武士 (Neon Samurai)",
            "prompt_type": "VISUAL",
            "price": 5.0,
            "usage_count": 482,
            "rating": 4.9
        }
    ]

# 初始化
init_sample_data()
