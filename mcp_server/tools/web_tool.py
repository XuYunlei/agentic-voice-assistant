import os, httpx

SEARCH_PROVIDER = os.getenv("SEARCH_PROVIDER", "brave")
API_KEY = os.getenv("SEARCH_API_KEY")

BRAVE_URL = "https://api.search.brave.com/res/v1/web/search"

def web_search(query: str, top_k: int = 5):
    if not API_KEY:
        return []

    if SEARCH_PROVIDER == "brave":
        return brave_search(query, top_k)

    return []  # fallback


def brave_search(query, top_k):
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": API_KEY
    }

    params = {
        "q": query,
        "count": top_k
    }

    try:
        with httpx.Client(timeout=20) as client:
            resp = client.get(BRAVE_URL, headers=headers, params=params)
            resp.raise_for_status()
            data = resp.json()
    except Exception as e:
        print("[web.search] Brave error:", e)
        return []

    # Normalize output for the agent
    results = []
    for item in data.get("web", {}).get("results", [])[:top_k]:
        results.append({
            "title": item.get("title"),
            "url": item.get("url"),
            "snippet": item.get("description"),
            "profile": item.get("profile", {}).get("name"),
            "price": None,
            "availability": None
        })

    return results
