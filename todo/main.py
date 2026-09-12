from  fastapi import FastAPI,Depends,HTTPException,status,Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import Base,engine,get_db
from models import Todo
from schemas import TodoCreate,TodoResponse,TodoUpdate,TodoPatch
from typing import Literal

app = FastAPI()


Base.metadata.create_all(bind = engine)
# todos = [

# ]

# next_id = 1


@app.get("/")
def home():
    return {'message': 'Hello FastAPI'}


@app.post('/todos',response_model = TodoResponse,status_code=status.HTTP_201_CREATED)
def create_todo(todo:TodoCreate,db:Session = Depends(get_db)):
    # global next_id

    new_todo = Todo(
        # 'id': next_id,
        title=todo.title,
        description=todo.description,
        completed=todo.completed
    )
    # todos.append(new_todo)
    # next_id += 1
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@app.get("/todos", response_model=list[TodoResponse])
def get_todos(
    completed: bool | None = None,
    limit: int = Query(10, ge=1, le=100),
    skip: int = Query(0, ge=0),
    sort: Literal["id", "title", "completed"] = "id",
    order: Literal["asc", "desc"] = "asc",
    db: Session = Depends(get_db)
):
    query = db.query(Todo)

    if completed is not None:
        query = query.filter(Todo.completed == completed)

    if sort == "id":
        sort_column = Todo.id

    elif sort == "title":
        sort_column = Todo.title

    else:
        sort_column = Todo.completed

    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column)

    query = query.offset(skip)
    query = query.limit(limit)

    todos = query.all()

    return todos
@app.get("/todos/{todo_id}",response_model = TodoResponse,status_code=status.HTTP_200_OK)
def get_todo(todo_id:int,db:Session = Depends(get_db)):
    # for todo in todos:
    #     if todo['id'] == todo_id:
    #         return todo

    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        return todo
    else:
        raise HTTPException(status_code=404, detail="Todo not found")

@app.put('/todos/{todo_id}',response_model = TodoResponse,status_code=status.HTTP_200_OK)
def update_todo(todo_id:int,todo_data:TodoUpdate,db:Session = Depends(get_db)):

    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    # for exsiting_todo in todos:
    #     if exsiting_todo['id'] == todo_id:
    #         exsiting_todo['title'] = todo.title
    #         exsiting_todo['description'] = todo.description
    #         exsiting_todo['completed'] = todo.completed

    if todo:
        todo.title = todo_data.title
        todo.description = todo_data.description
        todo.completed = todo_data.completed
        db.commit()
        db.refresh(todo)
        return todo
    else :
        raise HTTPException(status_code=404, detail="Todo not found")
            # return exsiting_todo



@app.delete('/todos/{todo_id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id:int,db:Session = Depends(get_db)):
    # for todo in todos:
    #     if todo['id'] == todo_id:
    #         todos.remove(todo)
    #         return {'message':'Todo is deleted'}

    # return {'message':'Todo not found'}

    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if todo:
        db.delete(todo)
        db.commit()
        return {'message':'Todo is deleted'}
    else:
        raise HTTPException(status_code=404, detail="Todo not found")

        

@app.patch('/todos/{todo_id}',response_model = TodoResponse,status_code=status.HTTP_200_OK)
def patch_todo(
    todo_id:int,
    todo_data:TodoPatch,
    db:Session = Depends(get_db)
):

    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if todo is None :
        raise HTTPException(status_code=404,detail='Todo not found')

    if todo_data.title is not None:
        todo.title = todo_data.title

    if todo_data.description is not None:
        todo.description = todo_data.description

    if todo_data.completed is not None:
        todo.completed = todo_data.completed

    db.commit()
    db.refresh(todo)

    return todo