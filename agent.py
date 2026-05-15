from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()

# Initialize the model
llm = ChatOpenAI(model="gpt-4o-mini", max_tokens=1000, temperature=0)

# In-memory store for conversation sessions
store = {}

def get_chat_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# Build the prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# Chain prompt + model
chain = prompt | llm

# Wrap with history management
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_chat_history,
    input_messages_key="input",
    history_messages_key="history"
)

# --- Run a conversation ---
session_id = "dylan_session_1"

print("Chatbot ready. Type 'quit' to exit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break

    response = chain_with_history.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": session_id}}
    )
    print(f"AI: {response.content}\n")

# Print full history at the end
print("\n--- Conversation History ---")
for msg in store[session_id].messages:
    print(f"{msg.type.upper()}: {msg.content}")