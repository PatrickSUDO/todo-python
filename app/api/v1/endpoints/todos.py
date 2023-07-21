from fastapi import APIRouter, HTTPException
from app.db.models import Todo as TodoModel
from app.db.database import database
from app.schemas.todos import Todo as TodoSchema
from typing import List

router = APIRouter()


@router.post("/", response_model=TodoSchema)
async def create_todo(todo: TodoSchema):
    query = TodoModel.__table__.insert().values(
        task=todo.task,
        completed=todo.completed,
        deleted=todo.deleted
    )
    last_record_id = await database.execute(query)
    return {**todo.dict(), "id": last_record_id}


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
        .values(
            task=todo.task,
            completed=todo.completed,
            deleted=todo.deleted
        )
        .returning(TodoModel.__table__)
    )
    return await database.fetch_one(query)


@router.delete("/{todo_id}", response_model=TodoSchema)
async def delete_todo(todo_id: int):
    query = (
        TodoModel.__table__.update()
        .where(TodoModel.id == todo_id)
        .values(deleted=True)
        .returning(TodoModel.__table__)
    )
    return await database.fetch_one(query)
