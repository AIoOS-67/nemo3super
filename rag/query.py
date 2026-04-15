"""Ask Nemotron a question using your private knowledge base."""
import os
import sys
from pathlib import Path
import chromadb
from dotenv import load_dotenv
from openai import OpenAI
from embedder import embed

load_dotenv()

ROOT = Path(__file__).parent.parent
DB_DIR = ROOT / "chroma_db"
TOP_K = 8

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.environ["NVIDIA_API_KEY"],
)


def retrieve(question: str) -> list[dict]:
    col = chromadb.PersistentClient(path=str(DB_DIR)).get_or_create_collection("knowledge_base")
    if col.count() == 0:
        return []
    qvec = embed([question], input_type="query")[0]
    res = col.query(query_embeddings=[qvec], n_results=TOP_K)
    return [
        {"text": doc, "source": meta["source"]}
        for doc, meta in zip(res["documents"][0], res["metadatas"][0])
    ]


def ask(question: str):
    hits = retrieve(question)
    if hits:
        context = "\n\n".join(f"[{h['source']}]\n{h['text']}" for h in hits)
        system = (
            "You are a sharp, helpful assistant. Extract and synthesize answers from the "
            "[Knowledge Base] — reason across multiple snippets, compare sources, and make "
            "supported inferences. Quote exact numbers/names when present. If the KB truly "
            "has nothing relevant, say so briefly and offer a concise general-knowledge "
            "answer labeled '(general knowledge, not from KB)'. Cite source file(s). "
            "Reply in the user's language.\n\n"
            f"[Knowledge Base]\n{context}"
        )
        print(f"\n[Retrieved] {len(hits)} snippet(s) from: {sorted({h['source'] for h in hits})}")
    else:
        system = "You are a helpful assistant. (Note: the knowledge base is empty; answer from general knowledge.) Reply in the user's language."
        print("\n[!] Knowledge base is empty — answering from general knowledge.")

    print(f"\n[Question] {question}\n[Answer]")
    stream = client.chat.completions.create(
        model="nvidia/nemotron-3-super-120b-a12b",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": question},
        ],
        temperature=0.6,
        top_p=0.95,
        max_tokens=2048,
        frequency_penalty=0.3,
        presence_penalty=0.1,
        extra_body={"chat_template_kwargs": {"enable_thinking": False}},
        stream=True,
    )
    buf = ""
    past_think = False
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            piece = chunk.choices[0].delta.content
            if past_think:
                print(piece, end="", flush=True)
                continue
            buf += piece
            if "</think>" in buf:
                print(buf.split("</think>", 1)[1], end="", flush=True)
                past_think = True
            elif "<think>" not in buf and len(buf) > 20:
                # no thinking tags detected, safe to flush
                print(buf, end="", flush=True)
                buf = ""
                past_think = True
    if not past_think and buf:
        print(buf, end="", flush=True)
    print("\n")


if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) or "What do you think of Tesla's IPO?"
    ask(q)
