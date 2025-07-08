from fastapi import FastAPI, Request
import json
import os
import requests
import firebase_admin
from firebase_admin import credentials, firestore

app = FastAPI()

# ==== Model Selection ====
def select_model(prompt: str) -> str:
    p = prompt.lower()
    if any(w in p for w in ["code", "debug", "function", "python"]):
        return "deepseek/deepseek-chat:free"
    elif any(w in p for w in ["essay", "report", "pdf", "analyze"]):
        return "mistralai/mistral-nemo:free"
    elif any(w in p for w in ["reason", "plan", "think", "strategy"]):
        return "qwen/qwen3-235b-a22b:free"
    elif any(w in p for w in ["math", "solve", "teach"]):
        return "deepseek/deepseek-chat:free"
    elif any(w in p for w in ["open", "close", "launch"]):
        return "google/gemma-3-27b-it:free"
    return "qwen/qwen3-32b:free"

# ==== LLM Response ====
def get_ai_response(prompt):
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
    model = select_model(prompt)

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://your-zex.com",  # Optional
        "X-Title": "Cloud ZEX AI"
    }

    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }

    res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    if res.ok:
        return res.json()['choices'][0]['message']['content']
    else:
        return f"Error: {res.status_code} - {res.text}"

# ==== API Endpoint ====
@app.post("/chat")
async def chat(req: Request):
    data = await req.json()
    prompt = data.get("message", "")

    # First check memory logic
    mem_response = handle_memory(prompt)
    if mem_response:
        return {"reply": mem_response, "source": "memory"}

    # Then use AI
    ai_response = get_ai_response(prompt)
    return {"reply": ai_response, "source": "llm"}
