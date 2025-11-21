# Agentic Voice-to-Voice Product Discovery Assistant

End-to-end demo: voice input → agentic planning with LangGraph → RAG over Amazon 2020 slice via MCP → optional live web comparison → grounded, cited answer → TTS playback.

## Quick Start
1) Create and activate a Python 3.10+ venv
2) `pip install -r requirements.txt`
3) Copy `.env.example` to `.env` and fill keys (SEARCH_API_KEY, OPENAI_API_KEY if using TTS)
4) Build the local vector index: `bash scripts/build_index.sh`
5) In **Terminal A**, start MCP server: `bash scripts/run_mcp.sh`
6) In **Terminal B**, start the UI: `bash scripts/run_ui.sh`

> Sample data is included (10 mock products) so you can run without Kaggle on first boot.

Original tried Serper, but my API key does not have permissions for ANYTHING we need, so I switched to Brave. 