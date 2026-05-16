# 01 — Simple Conversational Agent

A context-aware AI assistant with persistent memory, built with LangChain, FastAPI, and GPT-4o Mini. This is the first agent in my AI Agents series — a clean foundation demonstrating how to wire a language model into a production-ready API with a custom chat UI.

🔗 **[Live Demo](https://dypintado.github.io/01-simple-conversational-agent/)**

---

## What It Does

- Maintains conversation history across messages using LangChain's `RunnableWithMessageHistory`
- Each user session gets its own isolated memory store
- Responds to any prompt — general knowledge, questions, analysis, conversation
- Clean chat UI with pulsing typing indicator and session persistence

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | GPT-4o Mini (OpenAI) |
| Agent Framework | LangChain |
| Backend | FastAPI + Uvicorn |
| Frontend | Vanilla HTML/CSS/JS |
| Backend Hosting | Railway |
| Frontend Hosting | GitHub Pages |

---

## Architecture

```
User (Browser)
     │
     │  POST /api/chat  { message, session_id }
     ▼
FastAPI Backend (Railway)
     │
     ├── RunnableWithMessageHistory
     │       └── Retrieves session history from in-memory store
     │
     ├── ChatPromptTemplate
     │       └── System prompt + history + user input
     │
     └── ChatOpenAI (GPT-4o Mini)
             └── Returns response → { response: "..." }
     │
     ▼
User (Browser) — displays AI response
```

---

## How Memory Works

LangChain's `RunnableWithMessageHistory` wraps the chain and automatically:
1. Fetches the conversation history for the current `session_id`
2. Injects it into the prompt as context
3. Appends the new human/AI message pair after each turn

Each browser session generates a unique `session_id`, so multiple users can chat simultaneously without their histories mixing.

---

## Running Locally

**1. Clone the repo**
```bash
git clone https://github.com/dypintado/01-simple-conversational-agent.git
cd 01-simple-conversational-agent
```

**2. Create a virtual environment and install dependencies**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

**3. Add your environment variables**
```bash
# Create a .env file
OPENAI_API_KEY=sk-...
```

**4. Start the backend**
```bash
uvicorn main:app --reload
```

**5. Open the frontend**

Open `index.html` in your browser or serve it locally. Update `API_URL` in the script to `http://localhost:8000/api/chat`.

---

## Project Structure

```
├── main.py          # FastAPI app — routes, LangChain chain, memory store
├── agent.py         # Standalone agent logic (notebook-style reference)
├── index.html       # Chat UI — sessions, typing indicator, message rendering
├── Procfile         # Railway deployment config
├── requirements.txt # Python dependencies
└── .env             # API keys (not committed)
```

---

## Part of My AI Agents Series

This is Agent #01 in a series of progressively complex AI agents I'm building and deploying. Each one introduces new concepts — memory, tools, RAG, multi-agent orchestration, and more.

| # | Agent | Concepts |
|---|-------|---------|
| 01 | Simple Conversational Agent | LLM chains, conversation memory |
| 02 | Coming soon | Tools + function calling |
| 03 | Coming soon | RAG + vector search |

---

Built by [Dylan Pintado](https://dylanpintado.com)
