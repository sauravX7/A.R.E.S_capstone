# Autonomous Multi-Agent System for Deep Research & EDA

A YAML-driven Hierarchical Orchestrator-Worker Architecture for automating complex research and Exploratory Data Analysis (EDA) tasks.

## 🎯 Problem Statement & Objectives

Manual research and EDA are highly repetitive, time-consuming tasks. Current singular LLMs struggle with multi-step workflows requiring tool use, code execution, and large context windows.

### Objectives
* Build a scalable **Multi-Agent System** using the Orchestrator/Worker pattern.
* Define agent behaviors and constraints modularly using **YAML schemas**.
* Automate the pipeline from web scraping to statistical analysis (EDA) and report synthesis.

### Scope & Outcome
* **Scope**: Focus on local execution (Ollama/Llama) for privacy, utilizing tools for web search, parsing, and isolated Python code execution.
* **Outcome**: A robust API/Frontend where users submit complex queries, and specialized agents collaboratively produce a synthesized, data-backed report.

## 🏗️ System Architecture

* **Orchestrator**: Acts as the manager, parsing the initial prompt and delegating YAML-defined tasks.
* **Scraper Agent**: Uses tools to search the web, extract text/CSV data, and store it locally.
* **EDA Agent**: Operates in an isolated Python environment to execute code for statistical analysis on extracted datasets.
* **Synthesizer Agent**: Queries ChromaDB and EDA outputs to compile a cohesive final report.

## 💻 System Requirements

### Hardware
* **CPU**: Multi-core processor (min 8 cores)
* **RAM**: 16GB minimum (32GB recommended for local LLM inference)
* **GPU**: Nvidia RTX 3060+ (8GB+ VRAM) preferred for hardware acceleration

### Software Stack
* **Language**: Python 3.10+
* **Orchestration**: CrewAI / LangGraph
* **Backend**: FastAPI
* **Data Tools**: Pandas, Matplotlib, BeautifulSoup

### AI Models & DB
* **Local Engine**: Ollama
* **Core Model**: Llama 3.2 (or similar quantized models)
* **Vector Store**: ChromaDB (for context retrieval)
* **Config**: YAML for agent/task definitions

## 📅 Project Timeline (12 Weeks)
* **Weeks 1-2**: Architecture design & YAML schema definitions.
* **Weeks 3-5**: Tool development & isolated worker testing (Scraper, EDA).
* **Weeks 6-8**: Orchestrator implementation & state flow integration.
* **Weeks 9-10**: FastAPI backend & Frontend UI development.
* **Weeks 11-12**: System testing, benchmarking, & final documentation.

## 🚀 Usability & Applications
* **Market Intelligence**: Automate competitive analysis by scraping competitor websites, processing pricing data, and generating comprehensive market trend reports overnight.
* **Academic Research**: Accelerate literature reviews by deploying agents to find, summarize, and cross-reference hundreds of academic papers on a specific scientific topic.
* **Financial Analysis**: Extract tabular data from quarterly earnings reports, execute local pandas scripts to identify anomalies, and synthesize findings into investment summaries.
* **Private Data Exploration**: Safely perform EDA on sensitive internal company data without risking exposure to public cloud APIs, thanks to local LLM inference.

## 👥 Team Contributions
* **Member 1 (AI Architect & Orchestration)**: Design YAML schemas, implement CrewAI/LangGraph logic, prompt engineering.
* **Member 2 (Data Engineering & Tooling)**: Develop Scraper agent tools, isolated Python execution environment for EDA.
* **Member 3 (Backend & Integration)**: Build FastAPI layer, integrate ChromaDB, handle asynchronous task states.
* **Member 4 (Frontend & QA)**: Develop user interface (Streamlit/UI), benchmarking, system testing.

## 📚 References & Resources
* [CrewAI Documentation](https://docs.crewai.com/)
* [LangGraph](https://python.langchain.com/docs/langgraph)
* [Ollama](https://ollama.com/)
* ReAct Pattern: Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models"
* Retrieval-Augmented Generation (RAG): Lewis et al.
* Agentic Design Patterns: Andrew Ng discussions on AI Agentic Workflows.

## ⚙️ YAML Configuration System

A.R.E.S. is designed around a strictly validated YAML configuration system. This decouples the agent definitions from the core Python logic, allowing agents and workflows to be tuned without changing code.

### Where configurations are stored
*   `configs/workflows/`: Contains the routing logic and entry points for the multi-agent system.
*   `configs/agents/`: Contains the specific capabilities, prompts, and constraints for each agent.

### How it works
1.  **YAML Parsing**: At startup, `backend/app/core/config_loader.py` reads the YAML files.
2.  **Pydantic Validation**: The parsed YAML is strictly validated against schemas in `backend/app/models/schemas.py`. Invalid schemas, missing fields, or unknown tools are immediately rejected.
3.  **Tool Registry**: Agents can only be assigned tools that exist in the `backend/app/core/tool_registry.py`. This ensures YAML files cannot arbitrarily execute unverified Python code.
4.  **LangGraph Integration**: The validated Python objects are injected into the LangGraph state (`AgentState`), where the Orchestrator uses the routing rules to direct traffic.

### How Orchestrator Routing Works
The Orchestrator acts as the deterministic brain of A.R.E.S. 
1.  **Structured Output**: Instead of relying on free-form text, the Orchestrator LLM is strictly constrained via `with_structured_output` to return a `RoutingDecision` Pydantic model (`next_agent` and `reason`).
2.  **YAML Destination Control**: The LLM's chosen `next_agent` is immediately checked against the `routing_rules` defined in `configs/workflows/main_workflow.yaml`.
3.  **Conditional Edge Execution**: If the destination is valid, LangGraph's conditional edge transitions the graph to the chosen agent. If it is invalid (or if the LLM hallucinates an unknown agent), the error is caught, stored in the state, and the graph safely routes to `END` to prevent arbitrary code execution or loops.

## 🕷️ Scraper Agent & Data Collection

The Scraper Agent is responsible for retrieving and normalizing external data into strictly defined artifacts.

### Controlled Tool Execution
The Scraper Agent is bound by strict execution policies:
*   It can **only** execute tools listed in `configs/agents/scraper.yaml` (currently `fetch_and_extract_url` and `save_scraped_data`).
*   It operates in a bounded execution loop (max 3 iterations) to prevent infinite reasoning loops.

### Artifact Contract
When data is saved, it is written to the `data/raw/` directory. The Scraper generates a Pydantic `CollectedArtifact` representing the provenance of the data:
*   `artifact_id`: A UUID.
*   `artifact_type`: E.g., `TXT`, `CSV`.
*   `source_url`: The URL the data was retrieved from.
*   `retrieval_timestamp`: Timestamp of collection.
*   `path`: The absolute path to the safely stored file.

This artifact is then injected into the LangGraph `AgentState["collected_data"]` dictionary, creating a deterministic contract that the future EDA Agent can consume without needing to re-scrape or guess file paths.

### Security
*   **Path Traversal Prevention**: The storage module strictly enforces that all writes remain within `data/raw/`. Any attempt to write to `../../` will raise an immediate error.
*   **Arbitrary Execution**: The agent cannot execute raw Python or shell commands. It must use the explicitly provided LangChain `@tool` functions.

## 📊 EDA Agent & Execution Architecture

The EDA Agent is responsible for analyzing the artifacts collected by the Scraper Agent. Because data analysis frequently involves executing code, the A.R.E.S. capstone implements a **dual-mode security architecture** to ensure the LLM cannot compromise the host environment.

### 1. Controlled Mode (Default)
By default (`EDA_EXECUTION_MODE=controlled`), the LLM **cannot write or execute arbitrary Python**. Instead, it generates a structured `EDARequest` that selects from a whitelist of deterministic, safe Pandas operations:
*   `inspect_dataset`: Extracts dimensions, column types, and missing value counts.
*   `missing_values_analysis`: Provides granular missing value statistics.
*   `descriptive_statistics`: Generates standard statistical summaries.

**Security**: High. The execution boundary is enforced structurally. The application intercepts the LLM's request and executes the predefined Python function natively, entirely preventing arbitrary code generation.

### 2. Untrusted Subprocess Mode (Experimental)
For development and experimentation (`EDA_EXECUTION_MODE=untrusted_subprocess`), the LLM may use the `custom_code` operation to write arbitrary Pandas code. 
*   The code is injected into a temporary file alongside paths to approved datasets.
*   The file is executed in a separate `python` subprocess with a strict **10-second timeout** and bounded output limits.

> **⚠️ SECURITY LIMITATION**: This is a **DEVELOPMENT-ONLY** convenience. It **DOES NOT** provide strong sandbox security. It runs as the current OS user and does not natively prevent the generated code from accessing host files, environment variables, or the network. It exists solely because a true Docker sandbox could not be guaranteed in the local environment.

### Artifact Integration
EDA results are appended to `AgentState["analysis_results"]` using the `EDAResult` schema, natively embedding `CollectedArtifact` objects to ensure provenance is carried fully intact to the final Synthesizer step.

## 🛠️ Setup Instructions

Follow these steps to run the A.R.E.S. Capstone project locally.

### 1. Repository Structure
The project is a monorepo consisting of a Next.js frontend and a FastAPI backend:
- `frontend/`: Next.js (App Router, Tailwind, TypeScript)
- `backend/`: FastAPI, LangGraph, Ollama integration

### 2. Backend Setup
1. Open a terminal and navigate to the project root.
2. Create and activate a Python virtual environment:
   ```bash
   # macOS/Linux
   python3 -m venv backend/.venv
   source backend/.venv/bin/activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
4. Configure the environment variables:
   ```bash
   cp backend/.env.example backend/.env
   ```
   *(Edit `backend/.env` if your Ollama instance runs on a different port/model)*

5. Start the local LLM (Ollama):
   Ensure Ollama is installed and running on your machine with the configured model:
   ```bash
   ollama pull llama3.2
   ollama run llama3.2
   ```

6. Start the FastAPI server:
   ```bash
   # Ensure you are in the backend directory or specify the path
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### 3. Frontend Setup
1. Open a new terminal and navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install Node dependencies (if not already installed):
   ```bash
   npm install
   ```
3. Start the Next.js development server:
   ```bash
   npm run dev
   ```

### 4. Testing the Application
1. **Backend Health Check**: Open `http://localhost:8000/health` in your browser. It should return `{"status":"ok"}`.
2. **Frontend UI**: Open `http://localhost:3000` in your browser. You will see the A.R.E.S UI showing the backend connection status.
3. **Chat Interface**: Use the text input on the frontend to send a message. The request will travel through the FastAPI backend, hit the LangGraph node, and query your local Ollama model.
