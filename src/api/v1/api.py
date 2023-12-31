from fastapi import APIRouter

from src.api.v1.endpoints import todos

router = APIRouter()

router.include_router(todos.router, prefix="/todos", tags=["todos"])
