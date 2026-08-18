# 🚀 Ollama Installation Guide for A.R.E.S. Capstone

## What is Ollama?
Ollama is a lightweight framework for running large language models (LLMs) locally on your machine. The A.R.E.S. system uses Ollama to power the AI agents without requiring cloud API calls.

## Installation Steps

### 1. Download Ollama
- Visit: **https://ollama.ai**
- Click the **Download** button
- Select **Windows** (or your OS)
- Run the downloaded installer (OllamaSetup.exe)

### 2. Complete Installation
- Follow the installer prompts
- Once installed, Ollama will automatically start as a background service
- You should see the Ollama icon in your system tray (bottom-right)

### 3. Pull a Language Model

Open **PowerShell** (as regular user, not admin) and run one of these commands:

#### Option A: Llama2 (Recommended for quality, ~4GB)
```powershell
ollama pull llama2
```

#### Option B: Mistral (Faster, ~5GB)
```powershell
ollama pull mistral
```

#### Option C: Neural Chat (Fast & good quality, ~4GB)
```powershell
ollama pull neural-chat
```

The download will take a few minutes depending on your internet speed. You'll see a progress bar.

### 4. Verify Installation

Check that the model was downloaded:
```powershell
ollama list
```

You should see output like:
```
NAME            ID              SIZE    MODIFIED
llama2          73bbecd3bea0    3.8 GB  3 minutes ago
```

### 5. Verify Ollama Server is Running

Ollama runs as a service on `http://localhost:11434`. Test it with:
```powershell
curl http://localhost:11434/api/tags
```

You should get a JSON response listing your models.

### 6. Restart A.R.E.S. Backend

The backend will automatically detect Ollama on the next request. 

**Either:**
- Refresh your browser (http://localhost:3000)
- Or restart the backend terminal

### 7. Test the Full System

1. Go to http://localhost:3000
2. Enter a message in the chat box
3. Click "Send to LangGraph"
4. You should now get real responses from the LLM!

---

## Troubleshooting

### Ollama service not starting?
- Restart your computer
- Or start manually: Open PowerShell and run `ollama serve`

### Model download failing?
- Check your internet connection
- Ensure you have at least 5GB free disk space
- Try a smaller model like `neural-chat`

### Backend still showing "Mock response"?
- Wait a few seconds after pulling the model
- Refresh your browser
- Check Ollama is running: `ollama list` should show your models

---

## Next Steps

Once Ollama is running and a model is loaded, your A.R.E.S. system will:
1. Route user queries through the Orchestrator agent
2. Execute Scraper or EDA agents as needed
3. Synthesize responses using real LLM intelligence

Enjoy! 🎉
