from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="The Backend Cortex for G-AI Network",
    docs_url="/docs",       # Swagger UI 地址
    redoc_url="/redoc"
)

# 配置 CORS (允许 index.html 访问)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    print(">>> G-AI PROTOCOL INITIATED. WAITING FOR BEGGING REQUESTS...")