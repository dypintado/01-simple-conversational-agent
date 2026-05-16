from http.server import BaseHTTPRequestHandler
import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

conversation_store = {}

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = json.loads(body)

        message = data.get("message", "")
        session_id = data.get("session_id", "default")

        if session_id not in conversation_store:
            conversation_store[session_id] = []

        conversation_store[session_id].append({
            "role": "user",
            "content": message
        })

        messages = [{"role": "system", "content": "You are a helpful AI assistant built by Dylan Pintado."}] + conversation_store[session_id]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=1000
        )

        reply = response.choices[0].message.content

        conversation_store[session_id].append({
            "role": "assistant",
            "content": reply
        })

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"response": reply}).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()