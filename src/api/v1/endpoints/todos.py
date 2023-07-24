from typing import List
from fastapi import APIRouter, HTTPException, Response

from src.db.database import database
from src.db.models import Todo as TodoModel
from src.schemas.todos import Todo as TodoSchema

router = APIRouter()


@router.get("/completed", response_model=List[TodoSchema])
async def read_completed_todos():
    query = TodoModel.__table__.select().where(TodoModel.completed == True)
    return await database.fetch_all(query)


@router.get("/deleted", response_model=List[TodoSchema])
async def read_deleted_todos():
    query = TodoModel.__table__.select().where(TodoModel.deleted == True)
    return await database.fetch_all(query)


@router.post("/", response_model=TodoSchema, status_code=201)
async def create_todo(todo: TodoSchema):
    query = (
        TodoModel.__table__.insert()
        .values(task=todo.task, completed=todo.completed, deleted=False)
        .returning(TodoModel.__table__)
    )
    return await database.fetch_one(query)


@router.get("/", response_model=List[TodoSchema])
async def read_todos(show_deleted: bool = False):
    query = TodoModel.__table__.select().where(TodoModel.deleted == show_deleted)
    return await database.fetch_all(query)


@router.get("/{todo_id}", response_model=TodoSchema)
async def read_todo(todo_id: int):
    query = TodoModel.__table__.select().where(TodoModel.id == todo_id)
    todo = await database.fetch_one(query)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.put("/{todo_id}", response_model=TodoSchema)
async def update_todo(todo_id: int, todo: TodoSchema):
    query = (
        TodoModel.__table__.update()
        .where(TodoModel.id == todo_id)
        .values(task=todo.task, completed=todo.completed, deleted=todo.deleted)
        .returning(TodoModel.__table__)
    )
    return await database.fetch_one(query)


@router.delete("/{todo_id}", status_code=204)
async def delete_todo(todo_id: int):
    query = (
        TodoModel.__table__.update()
        .where(TodoModel.id == todo_id)
        .values(deleted=True)
        .returning(TodoModel.__table__)
    )
    deleted_todo = await database.fetch_one(query)
    if deleted_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return Response(status_code=204)


@router.get("/completed", response_model=List[TodoSchema])
async def read_completed_todos():
    query = TodoModel.__table__.select().where(TodoModel.completed == True)
    return await database.fetch_all(query)


@router.get("/deleted", response_model=List[TodoSchema])
async def read_deleted_todos():
    query = TodoModel.__table__.select().where(TodoModel.deleted == True)
    return await database.fetch_all(query)
