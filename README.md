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
