"""NVIDIA NIM embedder wrapper — uses nv-embedqa-e5-v5 via build.nvidia.com API."""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

NVIDIA_API_KEY = os.environ["NVIDIA_API_KEY"]
EMBED_URL = "https://integrate.api.nvidia.com/v1/embeddings"
EMBED_MODEL = "nvidia/nv-embedqa-e5-v5"


def embed(texts: list[str], input_type: str = "passage") -> list[list[float]]:
    """Embed a batch of texts. input_type = 'passage' for docs, 'query' for questions."""
    if isinstance(texts, str):
        texts = [texts]
    resp = requests.post(
        EMBED_URL,
        headers={
            "Authorization": f"Bearer {NVIDIA_API_KEY}",
            "Accept": "application/json",
        },
        json={
            "input": texts,
            "model": EMBED_MODEL,
            "input_type": input_type,
            "encoding_format": "float",
            "truncate": "END",
        },
        timeout=60,
    )
    if not resp.ok:
        raise RuntimeError(f"Embedding {resp.status_code}: {resp.text[:500]}")
    return [d["embedding"] for d in resp.json()["data"]]
