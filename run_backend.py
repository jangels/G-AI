#!/usr/bin/env python
"""
从项目根目录启动 backend 的包装脚本
用法: uv run run_backend.py
"""
import subprocess
import sys
from pathlib import Path

backend_dir = Path(__file__).parent / "backend"
run_script = backend_dir / "run.py"

# 切换到 backend 目录并运行
subprocess.run([sys.executable, str(run_script)], cwd=str(backend_dir))
