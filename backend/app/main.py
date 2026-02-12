from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
import traceback
import logging
from backend.app.core.config import settings
from backend.app.db import init_db
from backend.app.api.api import api_router

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    init_db()
    logger.info(f"API_V1_STR: {settings.API_V1_STR}")
    for route in app.routes:
        logger.info(f"Route: {route.path} {route.name}")
    yield

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json", lifespan=lifespan)

# Global exception handler
@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
        logger.error(f"Request: {request.method} {request.url}")
        logger.error(f"Traceback:\n{traceback.format_exc()}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": f"Internal server error: {str(e)}"}
        )

# FastAPI exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"FastAPI Exception Handler - Unhandled exception: {exc}")
    logger.error(f"Request: {request.method} {request.url}")
    logger.error(f"Traceback:\n{traceback.format_exc()}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Internal server error: {str(exc)}"}
    )


@app.get("/debug-routes")
def debug_routes():
    routes = []
    for route in app.routes:
        routes.append({"path": route.path, "name": route.name})
    return {"routes": routes, "api_v1_str": settings.API_V1_STR}

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

# Mount Frontend (Static Files) - MUST BE LAST
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
