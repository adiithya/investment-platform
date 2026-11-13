from fastapi import FastAPI

from app.api.routes import health, auth
from app.api.routes.portfolios import router as portfolios_router


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

app.include_router(
    portfolios_router, 
    prefix="/api"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to TradePulse API"
    }