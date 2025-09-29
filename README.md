# cloud-zex
# 🌌 Cloud ZEX AI Assistant

Cloud ZEX is a **JARVIS-like personal AI assistant** built with **FastAPI**, **OpenRouter LLMs**, and **Firebase Firestore** memory.
It is deployed on **Railway** and connected to **Telegram via n8n**, enabling you to chat with it anytime from anywhere.

---

## ✨ Features

* 🔗 **Telegram Integration** via n8n (chat with ZEX directly in Telegram)
* 🧠 **Persistent Memory** stored in Firebase Firestore
* 🤖 **Smart Model Routing** using OpenRouter free models

  * Coding/debug → DeepSeek Chat
  * Reasoning/planning → Qwen
  * General chat → Qwen-32B
  * Documents/analysis → Mistral-Nemo
  * Device actions → Gemma
* ⚡ **Deployed on Railway** for 24/7 availability
* 🎛 **Configurable via Environment Variables**

---

## 🛠️ Tech Stack

* **Backend:** Python (FastAPI)
* **AI Models:** OpenRouter API
* **Database:** Firebase Firestore
* **Hosting:** Railway
* **Automation:** n8n
* **Messaging:** Telegram Bot

---

## 📂 Project Structure

```
cloud-zex/
│── cloud_zex.py          # Main FastAPI app
│── requirements.txt      # Python dependencies
│── README.md             # Project documentation
```



## 🔗 Telegram Integration (via n8n)

1. Create a Telegram bot using [BotFather](https://t.me/botfather).
2. Add Telegram → Webhook node in n8n.
3. Connect the webhook to your Cloud ZEX `/chat` API.
4. Now you can chat with ZEX directly from Telegram!

---

## ⚠️ Notes

* Keep your `firebase_key.json` **private** (do not commit to public repos).
* Ensure the Firebase key JSON is properly escaped when setting as an env variable.
* Railway free tier may restart after inactivity; memory is persistent because Firestore is cloud-hosted.

---

## 📌 Future Improvements

* 🎙️ Voice input & output
* 📱 Android app for remote control
* 🖥️ GUI with orb animation
* 📂 Multi-modal input (images, documents)

---

## 👨‍💻 Author

Built by **Arsalan Ali** 🚀
