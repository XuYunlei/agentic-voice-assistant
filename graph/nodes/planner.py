def plan(state):
    intent = state["intent"] or {}
    constraints = intent.get("constraints") or {}
    filters = {"category": "Household Cleaning"}
    if constraints.get("budget"):
        filters["price"] = {"$lte": constraints["budget"]}
    plan = {
        "sources": ["rag.search"] + (["web.search"] if intent.get("needs_live") else []),
        "filters": filters,
        "fields": ["sku","title","price","rating","brand","ingredients"]
    }
    state.update(plan=plan)
    state["log"].append({"node":"planner","plan":plan})
    return state
