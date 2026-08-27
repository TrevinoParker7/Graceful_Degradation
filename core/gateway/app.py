from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from config.settings import config
from windows.filesystem.canary import canary_manager
from core.policy.engine import policy_engine
from .routes import router as api_router

DASHBOARD_DIR = Path(__file__).resolve().parent.parent.parent / "dashboard"

@asynccontextmanager
async def lifespan(app: FastAPI):
    config.ensure_directories()
    canary_manager.seed_canary_files()
    policy_engine.reload_policies()
    yield

app = FastAPI(
    title="GracefulOS Core",
    description="Windows 11 Local-Only Agentic AI Security Control Plane & Graceful Degradation OS",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:7777", "http://localhost:7777"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

if DASHBOARD_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(DASHBOARD_DIR)), name="static")

    @app.get("/")
    async def serve_dashboard():
        index_file = DASHBOARD_DIR / "index.html"
        return FileResponse(str(index_file))
