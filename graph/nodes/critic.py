def critique(state):
    # Safety & grounding checks
    if state.get("safety_flags"):
        state["answer"] = "I can help with product choices, but I can’t advise on unsafe chemical practices."
    if not any((c.get("source")=="private") for c in (state.get("citations") or [])):
        state["answer"] = "I couldn't verify results from the private catalog. Please try a different query."
    state["log"].append({"node":"critic","status":"ok"})
    return state
