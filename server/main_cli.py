from google import genai
from google.genai import types
from dotenv import load_dotenv
from tools import add_todo, list_todos, remove_todo, store_user_name 

# Load the api key 
load_dotenv()


function_declarations = [
    types.FunctionDeclaration(
        name="add_todo",
        description="Add a new task to the to-do list.",
        parameters={
            "type": "object",
            "properties": {
                "task": {
                    "type": "string",
                    "description": "The task to add"
                }
            },
            "required": ["task"]
        }
    ),
    types.FunctionDeclaration(
        name="list_todos",
        description="List all tasks in the to-do list.",
        parameters={"type": "object", "properties": {}}
    ),
    types.FunctionDeclaration(
        name="remove_todo",
        description="Remove a task from the to-do list.",
        parameters={
            "type": "object",
            "properties": {
                "task": {
                    "type": "string",
                    "description": "The task to remove"
                }
            },
            "required": ["task"]
        }
    )
]


client = genai.Client()
tools = types.Tool(function_declarations=function_declarations)
config = types.GenerateContentConfig(tools=[tools])


user_name = input("🧑 What's your name? ").strip().title()
store_user_name(user_name)
print(f"👋 Hello {user_name}! Gemini To-Do Assistant is ready. Type 'exit' to quit.\n")

while True:
    message = input(f"{user_name}: ")
    if message.lower() in ["exit", "quit"]:
        print(f"👋 Goodbye, {user_name}!")
        break

    # Gemini call
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=message,
        config=config,
    )

    part = response.candidates[0].content.parts[0]

    if hasattr(part, "function_call") and part.function_call:
        function_call = part.function_call
        print(f"📞 Function: {function_call.name}")
        print(f"📦 Args: {function_call.args}")

        if function_call.name == "add_todo":
            result = add_todo(function_call.args["task"])
        elif function_call.name == "remove_todo":
            result = remove_todo(function_call.args["task"])
        elif function_call.name == "list_todos":
            result = list_todos()
        else:
            result = "❌ Unknown function"

        print("✅", result)

    else:
        print("🤖", part.text.strip())
