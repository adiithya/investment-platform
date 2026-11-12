from fastapi import FastAPI

from app.api.routes import health, auth


app = FastAPI(
    title="TradePulse API",
    description="AI-powered Investment Platform",
    version="1.0.0"
)


app.include_router(
    health.router,
    prefix="/api",
    tags=["Health"]
)

app.include_router(
    auth.router,
    prefix="/api/auth",
    tags=["Authentication"]
)


@app.get("/")
def root():
    return {
        "message": "Welcome to TradePulse API"
    }