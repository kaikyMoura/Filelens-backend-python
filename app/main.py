import contextlib
import os
from fastapi import FastAPI
import uvicorn
from app.database import init_db, shutdown_db
from app.routes.user_route import router as user_router
from starlette.middleware.cors import CORSMiddleware


@contextlib.asynccontextmanager
async def on_startup(app: FastAPI):
    await init_db()
    print("✅ Filelens API online")
    yield
    await shutdown_db()
    print("🛑 Filelens API offline")


app = FastAPI(
    title="Filelens API",
    description="API for Filelens aplication",
    version="1.0.0",
    lifespan=on_startup,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["X-Custom-Header"],
)

app.include_router(user_router, prefix="/v1")


@app.get("/health")
async def health_check():
    try:
        return {"status": "healthy", "message": "✅ Filelens API is running"}
    except Exception as e:
        return {"status": "unhealthy", "message": f"🛑 Filelens API is offline"}


@app.get("/")
async def root():
    return {
        "message": "Welcome to the Filelens API",
        "details": "Acess the documentation at /docs",
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=os.environ.get("PORT", 8000))
