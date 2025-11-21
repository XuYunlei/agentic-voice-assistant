# Agentic Voice-to-Voice Product Discovery Assistant

End-to-end demo: voice input → agentic planning with LangGraph → RAG over Amazon 2020 slice via MCP → optional live web comparison → grounded, cited answer → TTS playback.


### **Phase 1 — Complete Pipeline**

Voice-to-Voice · RAG + Web Hybrid · MCP-Powered Agents

---

## 🚀 Overview

This project implements an **agentic multimodal product search assistant** using:

* **LangGraph** for multi-step agent orchestration
* **HuggingFace Amazon 2020 dataset** (15 columns — no rating, no reviews)
* **ChromaDB** vector index
* **MCP server** exposing RAG + Web Search tools
* **Brave Search API**
* **Whisper ASR** for speech
* **OpenAI TTS** for final spoken answers
* **Streamlit UI** for a voice-to-voice demo

The system takes a user’s voice input → converts to text → interprets intent → fetches products via RAG and/or web search → returns an answer → speaks the answer back.

**Phase 1 is 100% implemented and working.**

---

# 📁 Project Structure

```
agentic-voice-assistant/
│
├── app/
│   ├── ui_streamlit.py               # Main Streamlit voice UI
│   ├── audio_utils.py                # (optional placeholder)
│   └── components.py                 # (optional placeholder)
│
├── configs/
│   └── env.example
│
├── data/
│   ├── processed/products.csv        # HF Amazon 2020 dataset (15 cols)
│   └── index/                        # Chroma DB (auto-created)
│
├── graph/
│   ├── langgraph_pipeline.py
│   ├── schemas.py
│   └── nodes/
│       ├── router.py
│       ├── planner.py
│       ├── retriever.py
│       ├── answerer.py
│       └── critic.py
│
├── indexing/
│   └── build_index.py                # Build HF→Chroma vector index
│
├── mcp_server/
│   ├── server.py                     # FastAPI MCP server
│   └── tools/
│       ├── rag_tool.py
│       └── web_tool.py
│
├── prompts/
│   ├── system_router.md
│   ├── system_planner.md
│   ├── system_answerer.md
│   └── tool_call_instructions.md     # (empty for Phase 1)
│
├── scripts/
│   ├── build_index.sh
│   ├── run_mcp.sh
│   └── run_ui.sh
│
└── tts_asr/
    ├── asr_whisper.py
    └── tts_client.py
```

---

# 🔧 Installation & Setup

### 1️⃣ Create environment

```bash
conda create -n GenAI python=3.10 -y
conda activate GenAI
pip install -r requirements.txt
```

---

### 2️⃣ Add environment variables

Create `.env` using `configs/env.example` as a reference:

```
OPENAI_API_KEY=
BRAVE_API_KEY=
SEARCH_PROVIDER=brave

EMBED_MODEL=all-MiniLM-L6-v2
GEN_MODEL=openai/gpt-4o-mini

ASR_MODEL=small
TTS_PROVIDER=openai
TTS_VOICE=alloy

INDEX_PATH=./data/index
DATA_PRODUCTS=./data/processed/products.csv

MCP_BASE=http://127.0.0.1:8000
```

---

# 📦 Phase 1 Components

## 1️⃣ HF Dataset → Chroma Index

`indexing/build_index.py`:

* Renames HF fields:
  `Uniq Id → id`, `Product Name → title`, `Selling Price → price`, etc.
* Cleans price (`$` removal → float)
* Extracts `price_per_oz` if possible
* Ensures **all metadata is Chroma-safe**
* Adds docs to collection `amazon2020`

Build index:

```bash
bash scripts/build_index.sh
```

---

## 2️⃣ MCP Server (Tools)

Start MCP:

```bash
bash scripts/run_mcp.sh
```

### Tools exposed:

#### `/rag.search`

* Semantic search (SentenceTransformer)
* Optional price filters (`lte` / `gte`)
* Output fields:

  * `doc_id`
  * `title`
  * `price`
  * `brand` (placeholder)
  * `sku`

#### `/web.search`

* Brave Web API
* Returns:

  * `title`
  * `url`
  * `snippet`
  * `profile`

Test:

```bash
curl -X POST http://127.0.0.1:8000/rag.search \
  -H "Content-Type: application/json" \
  -d '{"query":"stainless steel cleaner"}'
```

---

## 3️⃣ Agent Workflow (LangGraph)

Workflow:
`router → planner → retriever → answerer → critic`

### router

* Classifies intent
* Decides:

  * RAG only
  * Web only
  * Both
* Extracts filters (brand, price)

### planner

* Ensures filters match HF (price only)
* Decides tool list

### retriever

* Calls MCP endpoints
* Stores RAG/Web evidence

### answerer

* HF dataset contains **NO ratings, ingredients, reviews**
* So answerer uses:

  * `title`
  * `price`
  * `brand` (empty)
* Sorts by **price only**
* Generates citations

### critic

* Placeholder for Phase 2 enhancements

---

## 4️⃣ Voice UI (Streamlit)

Run UI:

```bash
bash scripts/run_ui.sh
```

Features:

* Audio recording
* Whisper ASR
* Multi-agent reasoning
* Product results table
* Citations
* OpenAI TTS playback

Open browser:

```
http://localhost:8501
```

---

# 🔥 Next: Phase 2 Enhancements

Coming next:

* Tool Normalization Layer
* Conflict resolution engine
* Web–RAG merge logic
* Better product ranking
* Metadata extraction from web
* Price-per-oz ranking logic
* Safety + chemical constraints
* Critic rewrite for chain integrity
* LLM fallback for missing data
* Scoring systems for final answers
