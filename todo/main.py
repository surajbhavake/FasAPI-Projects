from  fastapi import FastAPI
from pydantic import BaseModel
from database import Base,engine
from models import Todo
app = FastAPI()


Base.metadata.create_all(bind = engine)
todos = [

]

next_id = 1


class Todo(BaseModel):
    id: int
    title : str
    description : str
    completed : bool

@app.get("/")
def home():
    return {'message': 'Hello FastAPI'}


@app.post('/todos')
def create_todo(todo:Todo):
    global next_id

    new_todo = {
        'id': next_id,
        'title': todo.title,
        'description':todo.description,
        'completed':todo.completed
    }
    todos.append(new_todo)
    next_id += 1
    return new_todo

@app.get('/todos')
def get_todos():
    return todos

@app.get("/todos/{todo_id}")
def get_todo(todo_id:int):
    for todo in todos:
        if todo['id'] == todo_id:
            return todo
    return {'message':'Todo not found'}


@app.put('/todos/{todo_id}')
def update_todo(todo_id:int,todo:Todo):

    for exsiting_todo in todos:
        if exsiting_todo['id'] == todo_id:
            exsiting_todo['title'] = todo.title
            exsiting_todo['description'] = todo.description
            exsiting_todo['completed'] = todo.completed

            return exsiting_todo

    return{'message':'Todo not found'}


@app.delete('/todos/{todo_id}')
def delete_todo(todo_id:int):
    for todo in todos:
        if todo['id'] == todo_id:
            todos.remove(todo)
            return {'message':'Todo is deleted'}

    return {'message':'Todo not found'}

        

