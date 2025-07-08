import json
import os

TODO_FILE = "memory.json"

def load_todos():
    try:
        with open(TODO_FILE, "r") as f:
            return json.load(f).get("todos", [])
    except FileNotFoundError:
        return []

def save_todos(todos):
    data = {}
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, "r") as f:
            data = json.load(f)
    data["todos"] = todos
    with open(TODO_FILE, "w") as f:
        json.dump(data, f)

def add_todo(task):
    todos = load_todos()
    todos.append(task)
    save_todos(todos)
    return f"📝 Added: {task}"

def remove_todo(task):
    todos = load_todos()
    if task in todos:
        todos.remove(task)
        save_todos(todos)
        return f"🗑️ Removed: {task}"
    return f"❌ Task not found: {task}"

def list_todos():
    todos = load_todos()
    return todos if todos else []

def store_user_name(name):
    data = {}
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, "r") as f:
            data = json.load(f)
    data["user_name"] = name
    with open(TODO_FILE, "w") as f:
        json.dump(data, f)

def get_user_name():
    try:
        with open(TODO_FILE, "r") as f:
            data = json.load(f)
            return data.get("user_name")
    except FileNotFoundError:
        return None
