# 🚀 Nemotron-RAG v0.1.0 — First Public Release

A **zero-config, privacy-first RAG chatbot** powered by NVIDIA **Nemotron 3 Super 120B**.
Download, double-click, drop in your files, and chat with your own docs — in your browser.

---

## ✨ Highlights

- 🧠 **Nemotron 3 Super 120B** via NVIDIA's free API (`build.nvidia.com`)
- 🔍 **RAG with source citations** — every answer shows which file it came from
- 🧩 **Multi-format ingestion** — `.pdf`, `.docx`, `.md`, `.txt`, `.py`, `.json`, `.html`
- 🌐 **Bilingual out of the box** — model replies in the language you ask in
- 🎛️ **Toggles** — RAG on/off, reasoning (thinking) mode on/off
- 👀 **Live re-indexing** — `watch.py` auto-re-embeds when files change
- 💻 **Cross-platform launchers** — `Start.bat` (Windows) / `Start.command` (macOS/Linux)
- 🔐 **Your docs stay local** — only embeddings + chat go over the wire

## 📥 Install in 3 Steps

1. Download **`Nemotron-RAG.zip`** below → extract anywhere
2. Get a free API key at [build.nvidia.com](https://build.nvidia.com) (search "nemotron-3-super")
3. **Windows:** double-click `Start.bat` · **macOS/Linux:** `./Start.command`

First launch takes 3–5 minutes to create a virtual environment and install dependencies. After that, it starts in seconds.

## 🗂️ Using Your Own Data

Drop files into the `docs/` folder. Then either:

```bash
python rag/ingest.py          # one-shot index
python rag/watch.py           # auto re-index on change
```

Open the browser tab and ask anything. The bot cites its sources.

## 🔧 What's Inside

| File | Role |
|------|------|
| `rag/app.py`       | Gradio web UI with multi-turn memory |
| `rag/ingest.py`    | Chunks + embeds docs into ChromaDB |
| `rag/query.py`     | One-shot CLI: `python query.py "..."` |
| `rag/watch.py`     | Daemon: auto re-index on file change |
| `rag/embedder.py`  | NVIDIA `nv-embedqa-e5-v5` wrapper |
| `chat.py`          | Terminal-only chat (no RAG) |
| `test_nemotron.py` | API smoke test |

## 🛣️ Roadmap

- [ ] `.xlsx` / `.csv` ingestion
- [ ] Drag-and-drop upload in the web UI
- [ ] Optional local fallback (Ollama) when NVIDIA API is unreachable
- [ ] Packaged `.exe` installer (PyInstaller)
- [ ] Hybrid BM25 + vector retrieval

## 🙏 Credits

Built on:
- **NVIDIA Nemotron 3 Super 120B** (LLM) + **nv-embedqa-e5-v5** (embeddings)
- **ChromaDB** — local vector store
- **Gradio** — UI framework
- **Watchdog** — file system events

Inspired by NVIDIA's "Agentic AI 101" / OpenClaw session at GTC 2026 — and by
[Julia Suzuki](https://www.linkedin.com/in/juliafsuzuki/)'s sharp LinkedIn recap
of that session, which was the direct spark for this project.

## 📜 License

MIT. Fork it, remix it, ship it.

---

**Feedback welcome!** Open an issue or drop a comment — this is v0.1, there's plenty to sharpen.
