from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Allow your website to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Same agent logic as before
llm = ChatOpenAI(model="gpt-4o-mini", max_tokens=1000, temperature=0)

store = {}

def get_chat_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant built by Dylan Pintado."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

chain = prompt | llm

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_chat_history,
    input_messages_key="input",
    history_messages_key="history"
)

# Define what a message request looks like
class MessageRequest(BaseModel):
    message: str
    session_id: str = "default"

@app.get("/")
def root():
    return {"status": "Agent is live"}

@app.post("/chat")
def chat(request: MessageRequest):
    response = chain_with_history.invoke(
        {"input": request.message},
        config={"configurable":{"session_id": request.session_id}}
    )
    return {"response": response.content}