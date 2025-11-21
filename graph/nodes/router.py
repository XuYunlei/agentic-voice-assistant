import re

SAFE_DENY = ["mixing chemicals", "medical claims"]

def route(state):
    text = (state.get("transcript") or "").strip()
    budget = None
    m = re.search(r'under\s*\$?(\d+(\.\d{1,2})?)', text, re.I)
    if m: budget = float(m.group(1))
    intent = {
        "task":"product_reco",
        "constraints":{
            "budget": budget,
            "material": "stainless steel" if "stainless" in text.lower() else None,
            "brand": None
        },
        "needs_live": any(k in text.lower() for k in ["now","today","in stock","availability","current price","latest"])
    }
    flags = [f for f in SAFE_DENY if f in text.lower()]
    state.update(intent=intent, safety_flags=flags)
    state.setdefault("log", []).append({"node":"router","intent":intent})
    return state
