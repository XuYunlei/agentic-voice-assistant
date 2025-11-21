from rapidfuzz import fuzz

def reconcile(rag_items, web_items):
    out = []
    for r in rag_items:
        match = None; score_best = 0
        for w in (web_items or []):
            s = fuzz.token_set_ratio(r.get("title",""), w.get("title",""))
            if s > score_best:
                score_best, match = s, w
        conflict = None
        out.append({"primary":r,"web_match":match,"score":score_best,"conflict":conflict})
    return out

def answer(state):
    rag = (state.get("evidence") or {}).get("rag", [])
    web = (state.get("evidence") or {}).get("web", [])
    rows = reconcile(rag, web)
    # Sort by rating desc then price asc (None-safe)
    def sort_key(x):
        pr = x["primary"]
        return (-(pr.get("rating") or 0), pr.get("price") if pr.get("price") is not None else 1e9)
    top = sorted(rows, key=sort_key)[:3]

    lines, cites = [], []
    for i, r in enumerate(top, 1):
        p = r["primary"]
        price = p.get("price","?")
        rating = p.get("rating","?")
        brand = p.get("brand") or "N/A"
        lines.append(f"{i}. {p['title']} — {rating}★, ${price} (brand: {brand})")
        cites.append({"doc_id": p.get("doc_id") or p.get("sku"), "source":"private"})
        if r["web_match"] and r["web_match"].get("url"):
            cites.append({"url": r["web_match"]["url"], "source":"web"})
    summary = "Here are options that fit your request. My top pick balances rating and price. See your screen for details."
    state.update(answer=summary + "\\n" + "\\n".join(lines), citations=cites)
    state["log"].append({"node":"answerer","top_k": len(top)})
    return state
