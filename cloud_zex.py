from fastapi import FastAPI, Request
import json
import uuid
import os
from pathlib import Path
import requests

app = FastAPI()

# ==== Memory ====
MEMORY_FILE = Path("memory.json")

def load_memory():
    if MEMORY_FILE.exists():
        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

memory = load_memory()

def handle_memory(command):
    lowered = command.lower()

    if lowered.startswith("remember"):
        parts = command.split("remember")[-1].strip().split(" is ")
        if len(parts) == 2:
            key, value = parts[0].strip(), parts[1].strip()
            memory[key] = value
            save_memory(memory)
            return f"Got it! I will remember {key} is {value}."

    elif lowered.startswith("forget"):
        key = command.split("forget")[-1].strip()
        if key in memory:
            del memory[key]
            save_memory(memory)
            return f"I forgot what {key} is."
        else:
            return f"I don't remember anything about {key}."

    elif lowered.startswith("what is") or lowered.startswith("who is"):
        key = command.split("is")[-1].strip()
        return memory.get(key, f"I don't remember {key}.")

    return None

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
        "HTTP-Referer": "https://your-zex.com",
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
        return f"Error: {res.status_code}"

# ==== API Routes ====
@app.post("/chat")
async def chat(req: Request):
    data = await req.json()
    prompt = data.get("message", "")

    mem_response = handle_memory(prompt)
    if mem_response:
        return {"reply": mem_response, "source": "memory"}

    ai_response = get_ai_response(prompt)
    return {"reply": ai_response, "source": "llm"}

