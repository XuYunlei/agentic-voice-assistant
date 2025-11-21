import os
import chromadb
from sentence_transformers import SentenceTransformer

INDEX_PATH = os.getenv("INDEX_PATH","./data/index")

client = chromadb.PersistentClient(path=INDEX_PATH)
col = client.get_or_create_collection("amazon2020")

def rag_search(query, top_k=5, filters=None):
    where = filters or {}
    res = col.query(query_texts=[query], n_results=top_k, where=where)
    out = []
    if not res["ids"] or not res["ids"][0]:
        return out
    for i in range(len(res["ids"][0])):
        meta = res["metadatas"][0][i] or {}
        out.append({
            "doc_id": res["ids"][0][i],
            "sku": meta.get("sku"),
            "title": res["documents"][0][i][:220],
            "price": meta.get("price"),
            "rating": meta.get("rating"),
            "brand": meta.get("brand"),
            "ingredients": meta.get("ingredients"),
        })
    return out
