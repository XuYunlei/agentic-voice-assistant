import os
import re
import pandas as pd
import chromadb
from chromadb.utils import embedding_functions

# Load paths
DATA_PRODUCTS = os.getenv("DATA_PRODUCTS", "./data/processed/products.csv")
INDEX_PATH = os.getenv("INDEX_PATH", "./data/index")


def normalize_price_per_oz(price, features):
    """Extract ounces from the text and compute price per ounce."""
    try:
        m = re.search(r"([\d.]+)\s*oz", str(features), re.I)
        ounces = float(m.group(1)) if m else None
        return float(price) / ounces if (price and ounces) else None
    except:
        return None


def safe_meta_value(v):
    """Ensure metadata contains only valid Chroma types."""
    if v is None:
        return ""
    if isinstance(v, float) and pd.isna(v):
        return ""
    if isinstance(v, (list, dict, tuple)):
        return str(v)
    return v


def build_docs(df: pd.DataFrame):
    """Convert HF DataFrame rows into (id, text, metadata) tuples."""
    docs = []

    # Rename HF columns to expected names
    df = df.rename(
        columns={
            "Uniq Id": "id",
            "Product Name": "title",
            "Category": "category",
            "Selling Price": "price",
            "About Product": "features",
        }
    )

    # Normalize price values
    df["price"] = df["price"].astype(str).str.replace("$", "", regex=False)
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    # Add price_per_oz if possible
    df["price_per_oz"] = df.apply(
        lambda r: normalize_price_per_oz(r.get("price"), r.get("features")), axis=1
    )

    for _, r in df.iterrows():
        # Build dense text document
        text = " ".join(
            [
                str(r.get("title", "")),
                str(r.get("features", "")),
                str(r.get("category", "")),
            ]
        )

        # Metadata dict — all passed through safe_meta_value
        meta = {
            "sku": safe_meta_value(r.get("id")),
            "brand": "",  # HF has no brand info
            "category": safe_meta_value(r.get("category")),
            "price": float(r.get("price")) if not pd.isna(r.get("price")) else 0.0,
            "rating": 0.0,  # HF missing rating column
            "ingredients": "",
            "price_per_oz": (
                float(r.get("price_per_oz"))
                if (r.get("price_per_oz") and not pd.isna(r.get("price_per_oz")))
                else 0.0
            ),
        }

        # Ensure ALL metadata fields are valid types
        meta = {k: safe_meta_value(v) for k, v in meta.items()}

        docs.append((str(r.get("id")), text, meta))

    return docs


if __name__ == "__main__":
    # Load dataset
    df = pd.read_csv(DATA_PRODUCTS)

    # Ensure index dir exists
    os.makedirs(INDEX_PATH, exist_ok=True)

    # Create persistent Chroma DB
    client = chromadb.PersistentClient(path=INDEX_PATH)

    # Embedding model
    emb = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=os.getenv("EMBED_MODEL", "all-MiniLM-L6-v2")
    )

    # Retrieve/create collection
    col = client.get_or_create_collection("amazon2020", embedding_function=emb)

    # Build docs list
    docs = build_docs(df)
    ids, texts, metas = zip(*docs)

    # Clear previous index
    existing = col.get()
    if len(existing["ids"]) > 0:
        col.delete(ids=existing["ids"])

    # Add all new items
    col.add(ids=list(ids), documents=list(texts), metadatas=list(metas))

    print(f"Indexed {len(ids)} items from HF dataset into Chroma collection 'amazon2020'.")