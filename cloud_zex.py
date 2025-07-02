import os
import json
import requests
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# ========== CONFIG ========== #
OPENROUTER_API_KEY =os.getenv("OPENROUTER_API_KEY")
MEMORY_FILE = "memory.json"

# ========== FASTAPI INIT ========== #
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ========== MEMORY SYSTEM ========== #
def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

memory = load_memory()

# ========== SMART MODEL ROUTING ========== #
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

# ========== CHAT MEMORY ========== #
chat_history = []

# ========== OPENROUTER LLM API ========== #
def get_ai_response(messages, model):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://your-zex.com",
        "X-Title": "Cloud ZEX"
    }
    data = {
        "model": model,
        "messages": messages
    }
    res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    return res.json()['choices'][0]['message']['content'] if res.ok else f"Error: {res.status_code}"

# ========== HANDLE MEMORY PROMPTS ========== #
def handle_memory_commands(prompt):
    lowered = prompt.lower()
    if lowered.startswith("remember"):
        parts = prompt.split("remember")[-1].strip().split(" is ")
        if len(parts) == 2:
            key, value = parts[0].strip(), parts[1].strip()
            memory[key] = value
            save_memory(memory)
            return f"Got it. I will remember {key} is {value}."
    elif lowered.startswith("forget"):
        key = prompt.split("forget")[-1].strip()
        if key in memory:
            del memory[key]
            save_memory(memory)
            return f"I forgot what {key} is."
        return f"I don't remember anything about {key}."
    elif lowered.startswith("what is") or lowered.startswith("who is"):
        key = prompt.split("is")[-1].strip()
        return memory.get(key, f"I don't remember {key}.")
    return None

# ========== API ROUTE ========== #
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("prompt", "").strip()
    if not user_input:
        return JSONResponse({"response": "Empty prompt"}, status_code=400)

    # Handle memory
    memory_response = handle_memory_commands(user_input)
    if memory_response:
        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": memory_response})
        return {"response": memory_response}

    # Model routing
    model = select_model(user_input)
    chat_history.append({"role": "user", "content": user_input})
    ai_response = get_ai_response(chat_history, model)
    chat_history.append({"role": "assistant", "content": ai_response})

    return {"response": ai_response}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))  # Render dynamically assigns a port
    uvicorn.run("cloud_zex:app", host="0.0.0.0", port=port, reload=False)
