#!/usr/bin/env python
"""
G-AI Backend 启动脚本
"""
import uvicorn
import sys
from pathlib import Path

# 获取当前脚本所在目录（backend目录）
backend_dir = Path(__file__).parent.absolute()

# 确保可以找到 app 模块
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

if __name__ == "__main__":
    # 热重载模式，方便开发
    print(f">>> Starting G-AI Backend from: {backend_dir}")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8001, reload=True)