from fastapi import FastAPI
from app.api.v1.api import router as api_v1_router
from app.api.health_check import router as health_check_router
from .db.database import database

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(api_v1_router, prefix="/api/v1")
app.include_router(health_check_router)
