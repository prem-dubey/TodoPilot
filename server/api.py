from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from tools import add_todo, list_todos, remove_todo, store_user_name, get_user_name  

load_dotenv()

app = FastAPI()

# CORS (React dev mode)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageRequest(BaseModel):
    message: str
    user_name: str | None = None  

# Gemini tool declarations
function_declarations = [
    types.FunctionDeclaration(
        name="add_todo",
        description="Add a task to the to-do list.",
        parameters={"type": "object", "properties": {"task": {"type": "string"}}, "required": ["task"]}
    ),
    types.FunctionDeclaration(
        name="list_todos",
        description="List all tasks.",
        parameters={"type": "object", "properties": {}}
    ),
    types.FunctionDeclaration(
        name="remove_todo",
        description="Remove a task from the list.",
        parameters={"type": "object", "properties": {"task": {"type": "string"}}, "required": ["task"]}
    )
]

tools = types.Tool(function_declarations=function_declarations)
config = types.GenerateContentConfig(tools=[tools])
client = genai.Client()

@app.post("/chat")
async def chat_with_gemini(payload: MessageRequest):
    message = payload.message.strip()
    if not message:
        return {
            "status": "error",
            "message": "Message cannot be empty."
        }


    stored_name = get_user_name()


    if not stored_name:
        if payload.user_name is None or payload.user_name.strip() == "":
            return {
                "status": "error",
                "message": "Please provide your name (only needed once)."
            }
        stored_name = payload.user_name.strip().title()
        store_user_name(stored_name)

    #  Gemini call
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=message,
        config=config,
    )

    part = response.candidates[0].content.parts[0]

    if hasattr(part, "function_call") and part.function_call:
        fn = part.function_call
        fn_name = fn.name
        fn_args = fn.args

        if fn_name == "add_todo":
            result = add_todo(fn_args["task"])
        elif fn_name == "remove_todo":
            result = remove_todo(fn_args["task"])
        elif fn_name == "list_todos":
            result = list_todos()
        else:
            result = "Unknown function"

        return {
            "status": "success",
            "type": "function",
            "function": fn_name,
            "response": result,
            "user_name": stored_name
        }

    return {
        "status": "success",
        "type": "text",
        "response": part.text.strip(),
        "user_name": stored_name
    }
