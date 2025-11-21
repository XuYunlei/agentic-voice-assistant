import os, httpx

def call_tool(path, payload):
    with httpx.Client(timeout=20) as c:
        r = c.post(path, json=payload)
        r.raise_for_status()
        return r.json().get("results", [])

def retrieve(state):
    base = os.getenv("MCP_BASE","http://127.0.0.1:8000")
    p = state["plan"]
    evidence = {}
    if "rag.search" in p["sources"]:
        evidence["rag"] = call_tool(f"{base}/rag.search", {
            "query": state["transcript"], "top_k": 5, "filters": p["filters"]
        })
    if "web.search" in p["sources"]:
        evidence["web"] = call_tool(f"{base}/web.search", {
            "query": state["transcript"], "top_k": 5
        })
    state.update(evidence=evidence)
    state["log"].append({"node":"retriever","evidence_keys": list(evidence.keys())})
    return state
