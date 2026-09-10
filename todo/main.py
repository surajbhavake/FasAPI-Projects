from  fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

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
