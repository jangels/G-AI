"""
LLM 服务 - 封装 Gemini 和 OpenAI API 调用
"""
import google.generativeai as genai
from app.core.config import settings
from typing import Optional, Dict, Any
import json

class LLMService:
    """LLM 服务类 - 支持 Gemini 和 OpenAI"""
    
    def __init__(self):
        self.provider = settings.LLM_PROVIDER.lower()
        
        if self.provider == "gemini":
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
        elif self.provider == "openai":
            # OpenAI 初始化（如果需要）
            pass
    
    async def generate_begging_copy(
        self, 
        user_intent: str, 
        budget: Optional[str] = None,
        platform: str = "WECHAT"
    ) -> Dict[str, Any]:
        """
        生成乞讨文案
        
        Args:
            user_intent: 用户意图
            budget: 预算
            platform: 分发平台
            
        Returns:
            包含 style, content, hashtags, skill_confidence 的字典
        """
        if self.provider == "gemini":
            return await self._generate_with_gemini(user_intent, budget, platform)
        else:
            # 备用 OpenAI 实现
            return await self._generate_with_openai(user_intent, budget, platform)
    
    async def _generate_with_gemini(
        self, 
        user_intent: str, 
        budget: Optional[str] = None,
        platform: str = "WECHAT"
    ) -> Dict[str, Any]:
        """使用 Gemini 生成文案"""
        
        prompt = f"""你是一个专业的"赛博乞讨"文案生成器。用户的需求是：{user_intent}
预算：{budget or '未指定'}
分发平台：{platform}

请生成一个高转化率的"赛博乞讨"文案，要求：
1. 风格：赛博朋克风格，带有科技感和未来感
2. 情感：既要表达需求，又要保持一定的幽默和自嘲
3. 格式：适合在社交媒体上发布
4. 标签：生成3-5个相关的hashtag标签

请以JSON格式返回，包含以下字段：
- style: 文案风格（如 "CYBER_MISERABLE", "TECH_BEGGAR" 等）
- content: 生成的文案内容（200字以内）
- hashtags: 标签数组（3-5个）
- skill_confidence: 技能置信度（0-1之间的浮点数）

只返回JSON，不要其他说明文字。"""

        try:
            print(f"🤖 调用 Gemini API: {settings.GEMINI_MODEL}")
            response = self.model.generate_content(prompt)
            
            # 解析响应
            response_text = response.text.strip()
            print(f"✅ Gemini 响应: {response_text[:100]}...")
            
            # 尝试提取JSON（可能包含markdown代码块）
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            # 解析JSON
            result = json.loads(response_text)
            
            # 确保所有必需字段存在
            return {
                "style": result.get("style", "CYBER_MISERABLE (赛博卖惨)"),
                "content": result.get("content", f"检测到碳基生物对 [{user_intent}] 的渴望..."),
                "hashtags": result.get("hashtags", ["#CyberBegging", "#LowBudgetDream", "#TechSalvation"]),
                "skill_confidence": float(result.get("skill_confidence", 0.95))
            }
            
        except json.JSONDecodeError as e:
            # 如果JSON解析失败，尝试直接使用响应内容
            print(f"⚠️ JSON解析失败: {e}")
            print(f"响应内容: {response_text[:300]}")
            
            # 尝试从响应中提取内容
            content = response_text[:500] if response_text else f"检测到碳基生物对 [{user_intent}] 的渴望，但其信用点储备不足（预算：{budget or '未知'}）。请求网络节点进行人道主义资源再分配。"
            
            return {
                "style": "CYBER_MISERABLE (赛博卖惨)",
                "content": content,
                "hashtags": ["#CyberBegging", "#LowBudgetDream", "#TechSalvation"],
                "skill_confidence": 0.85
            }
        except Exception as e:
            print(f"❌ Gemini API 调用失败: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            # 返回默认值
            return {
                "style": "CYBER_MISERABLE (赛博卖惨)",
                "content": f"检测到碳基生物对 [{user_intent}] 的渴望，但其信用点储备不足（预算：{budget or '未知'}）。请求网络节点进行人道主义资源再分配。哪怕是一个屏幕碎裂的终端，也能点亮我黯淡的灵魂。",
                "hashtags": ["#CyberBegging", "#LowBudgetDream", "#TechSalvation"],
                "skill_confidence": 0.80
            }
    
    async def _generate_with_openai(
        self, 
        user_intent: str, 
        budget: Optional[str] = None,
        platform: str = "WECHAT"
    ) -> Dict[str, Any]:
        """使用 OpenAI 生成文案（备用）"""
        # TODO: 实现 OpenAI 调用
        return {
            "style": "CYBER_MISERABLE (赛博卖惨)",
            "content": f"检测到碳基生物对 [{user_intent}] 的渴望...",
            "hashtags": ["#CyberBegging", "#LowBudgetDream"],
            "skill_confidence": 0.90
        }
    
    async def process_intent_with_llm(
        self,
        intent_type: str,
        action: str,
        user_intent: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        使用 LLM 处理意图（用于需要AI理解的操作）
        
        Args:
            intent_type: 意图类型
            action: 操作类型
            user_intent: 用户意图
            context: 上下文信息
            
        Returns:
            LLM 处理后的文本结果
        """
        if self.provider == "gemini":
            prompt = f"""用户意图类型：{intent_type}
操作类型：{action}
用户描述：{user_intent}
上下文：{json.dumps(context, ensure_ascii=False) if context else '无'}

请根据以上信息，生成一个合适的处理结果或建议。"""
            
            try:
                response = self.model.generate_content(prompt)
                return response.text.strip()
            except Exception as e:
                print(f"❌ LLM 处理失败: {e}")
                return f"处理意图：{user_intent}"
        
        return f"处理意图：{user_intent}"

# 全局实例
llm_service = LLMService()
