"""Gradio chat UI with RAG + multi-turn memory. Run: python app.py"""
import os
from pathlib import Path
import chromadb
import gradio as gr
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


def retrieve(question: str):
    col = chromadb.PersistentClient(path=str(DB_DIR)).get_or_create_collection("knowledge_base")
    if col.count() == 0:
        return [], 0
    qvec = embed([question], input_type="query")[0]
    res = col.query(query_embeddings=[qvec], n_results=TOP_K)
    hits = [
        {"text": doc, "source": meta["source"]}
        for doc, meta in zip(res["documents"][0], res["metadatas"][0])
    ]
    return hits, col.count()


def is_chitchat(msg: str) -> bool:
    """Short greetings/small talk skip RAG grounding."""
    m = msg.strip().lower()
    if len(m) < 8:
        return True
    greetings = ("hi", "hello", "你好", "在吗", "嗨", "哈喽", "hey", "在不", "good morning", "good evening", "thanks", "谢谢")
    return any(m.startswith(g) for g in greetings)


def respond(message, history, use_rag, thinking):
    chitchat = is_chitchat(message)
    hits, total = retrieve(message) if (use_rag and not chitchat) else ([], 0)

    if chitchat:
        system = "You are a friendly, concise personal assistant who knows the user's project knowledge base. For greetings or small talk, respond naturally — no need to cite the knowledge base. Answer in the user's language."
        sources_note = ""
    elif hits:
        context = "\n\n".join(f"[{h['source']}]\n{h['text']}" for h in hits)
        system = (
            "You are the user's sharp, helpful personal assistant. Your job is to extract and "
            "synthesize answers from the [Knowledge Base] below — do not be shy about reasoning "
            "across multiple snippets, connecting related facts, comparing sources, or making "
            "supported inferences. Quote exact numbers/names when they appear in the snippets. "
            "If the knowledge base truly has nothing relevant, say so briefly and then offer a "
            "concise general-knowledge answer clearly labeled '(general knowledge, not from KB)'. "
            "Always cite the source file(s) you pulled from. Reply in the same language the user used.\n\n"
            f"[Knowledge Base]\n{context}"
        )
        sources_note = f"\n\n---\n📚 {len(hits)} snippets cited / {total} total in KB / sources: {', '.join(sorted({h['source'] for h in hits}))}"
    else:
        system = "You are a helpful personal assistant. Reply in the user's language."
        sources_note = "\n\n---\n⚠️ RAG disabled" if not use_rag else "\n\n---\n⚠️ Knowledge base is empty"

    messages = [{"role": "system", "content": system}]
    for h in history:
        messages.append({"role": h["role"], "content": h["content"]})
    messages.append({"role": "user", "content": message})

    stream = client.chat.completions.create(
        model="nvidia/nemotron-3-super-120b-a12b",
        messages=messages,
        temperature=0.6,
        top_p=0.95,
        max_tokens=2048,
        frequency_penalty=0.3,
        presence_penalty=0.1,
        extra_body={"chat_template_kwargs": {"enable_thinking": thinking}},
        stream=True,
    )

    acc = ""
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            acc += chunk.choices[0].delta.content
            yield acc
    yield acc + sources_note


WECHAT_CSS = """
/* WeChat-style chat bubbles */
.gradio-container { background: #ededed !important; }
.message-row.user-row { justify-content: flex-end !important; }
.message-row.bot-row  { justify-content: flex-start !important; }

/* Bot bubble (left, white) */
.message.bot, .bot .message-content, .message-wrap .bot .message {
    background: #ffffff !important;
    color: #000 !important;
    border-radius: 4px 14px 14px 14px !important;
    max-width: 70% !important;
    padding: 10px 14px !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.06);
}

/* User bubble (right, WeChat green) */
.message.user, .user .message-content, .message-wrap .user .message {
    background: #95ec69 !important;
    color: #000 !important;
    border-radius: 14px 4px 14px 14px !important;
    max-width: 70% !important;
    padding: 10px 14px !important;
    margin-left: auto !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.06);
}

/* Avatar sizing */
.avatar-container img { width: 36px !important; height: 36px !important; border-radius: 4px !important; }

/* Tighten spacing */
.message-wrap { gap: 12px !important; }

/* Source-citation footer inside bot bubble — slightly dimmed */
.message.bot hr { border-color: #eee !important; margin: 10px 0 6px !important; }
"""

with gr.Blocks(title="Nemotron 3 Super x Private Knowledge Base") as demo:
    gr.Markdown("# 🧠 Nemotron 3 Super × Your Private Knowledge Base\nMulti-turn chat with memory · Auto-retrieves from everything in `docs/`")
    with gr.Row():
        use_rag = gr.Checkbox(value=True, label="Enable RAG retrieval")
        thinking = gr.Checkbox(value=False, label="Enable reasoning mode (slower)")
    gr.ChatInterface(
        fn=respond,
        additional_inputs=[use_rag, thinking],
        chatbot=gr.Chatbot(
            label="Conversation",
            height=560,
            show_label=False,
            avatar_images=(
                "https://api.dicebear.com/7.x/identicon/svg?seed=you",
                "https://api.dicebear.com/7.x/bottts/svg?seed=nemotron",
            ),
        ),
        textbox=gr.Textbox(placeholder="Ask anything about your documents...",
                           label="",
                           submit_btn="Send",
                           stop_btn="Stop"),
        examples=[
            ["What do you think of Tesla's IPO?", True, False],
            ["Summarize the key risks the bears pointed out.", True, False],
            ["Based on my docs, what are the top 3 takeaways?", True, True],
        ],
    )
    gr.Markdown("*Tip: drop new files into `docs/`, then run `python ingest.py` — or keep `python watch.py` running for auto-reindex.*")

if __name__ == "__main__":
    demo.launch(inbrowser=True, theme=gr.themes.Soft(), css=WECHAT_CSS)
