# ✈️ TodoPilot – AI-Powered To-Do List Manager

**TodoPilot** is an intelligent to-do assistant that helps you manage your tasks using natural language. Powered by **Google Gemini**, it understands your intent and allows you to add, remove, and view tasks through simple chat-style interactions.

Built with:
- ⚡️ React (Vite + TailwindCSS)
- 🧠 Google Gemini (via `google-genai`)
- 🚀 FastAPI (Python backend)

---

## 📸 Preview

![TodoPilot UI](https://res.cloudinary.com/dzwxshzzl/image/upload/v1752006513/Screenshot_2025-07-09_at_1.30.08_AM_i0kx5z.png) 

---

## ✨ Features

- ✅ Add tasks using AI (e.g. “Add ‘Buy milk’”)
- ✅ Remove tasks via natural language
- ✅ List current to-do items
- ✅ Remembers your name (asked only once)
- ✅ Gemini-powered intent parsing
- ✅ Chat-like interface with auto-scroll
- ✅ Clean, responsive design with Tailwind

---

React Frontend → FastAPI Backend → Gemini API → Python Tools (add/remove/list) → memory.json <br>

## 🧱 Architecture Diagram

```markdown

User → React Frontend (Vite + Tailwind)  
          ↓  
FastAPI Backend (`/chat` endpoint)  
          ↓  
Google Gemini 2.5 Flash API  
          ↓  
Structured Tool Calling  
          ↓  
tools.py (`add_todo`, `list_todos`, `remove_todo`)  
          ↓  
memory.json (task + username storage)
```

## 🚀 Set up Instructions 
### 📁 Clone the Repo
- cd TodoPilot
### 🔌 Backend Setup
- cd server
- python -m venv venv
- source venv/bin/activate 
- pip install -r requirements.txt
- create .env file and make it like .env-sample
- run the api server using ```uvicorn api:app --reload```
### 🌐 Frontend Setup (React + Tailwind)
- cd frontend
- Install all of the dependencies ```npm install```
- start the server using ```npm run dev```

## 🔧 Tool Call Integration

TodoPilot uses **structured tool calling** with Google Gemini.

The FastAPI backend registers these tools:

```python
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
)
```

## 🧠 Memory Handling

TodoPilot uses a local JSON file (`memory.json`) to persist user data across sessions.

### Structure:
```json
{
  "user_name": "Piyush",
  "todos": ["Buy groceries", "Finish homework"]
}
```

## 💬 Example Prompts
- "Add 'Buy milk'"
- "Delete 'Buy milk'"
- "What’s on my to-do list?"
- "Show my current tasks"
- "Add ‘Finish project demo’"


## ⚠️ Limitations & Future Enhancements
### ❌ Current Limitations
- Only supports one user (single memory file)
- Data stored in a local JSON file (no DB)
- No authentication
### 💡 Future Ideas
- Multi-user support with sessions or IDs
- Switch from memory.json to SQLite or Firebase
- Voice input and speech response
- Deploy backend to Render or Railway
- Deploy frontend to Vercel or Netlify







