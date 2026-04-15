# 🧠 Nemotron 3 Super × Your Private Knowledge Base

A zero-config, private RAG chatbot powered by **NVIDIA Nemotron 3 Super 120B**.
Drop your docs into `docs/`, chat with them in the browser — your data never leaves your machine (except the LLM call to NVIDIA's API).

## 🚀 Quick Start

### Windows
1. **Install Python 3.10+** from https://python.org (check "Add to PATH" during install)
2. **Get a free NVIDIA API key** at https://build.nvidia.com (Sign up → model page → "Get API Key")
3. **Double-click `Start.bat`**
4. On **first** run it will:
   - Create a virtual environment
   - Install dependencies (3–5 min)
   - Ask for your API key
   - Ingest whatever is in `docs/` into ChromaDB (one-time)
   - Open the chat UI in your browser

> **Re-indexing later** — Start.bat does NOT auto-detect new files on subsequent
> launches. After adding/editing docs, either run `python rag/ingest.py` once, or
> keep `python rag/watch.py` running for live re-indexing.

### macOS / Linux
```bash
chmod +x Start.command
./Start.command
```

## 📁 Adding Your Documents

Drop files into the `docs/` folder. Supported:
- `.txt` `.md` `.pdf` `.docx`
- `.py` `.json` `.html` (code / config)

Then either:
- **Manual**: run `python rag/ingest.py` once
- **Auto**: run `python rag/watch.py` in a second terminal — any file change re-indexes instantly

## 🎛️ Features

- ✅ Multi-turn chat with memory
- ✅ RAG retrieval with source citations (shows which file answered you)
- ✅ Thinking mode toggle (reasoning trace visible)
- ✅ Chinese + English mixed documents
- ✅ Works fully offline for ingestion; LLM calls go to NVIDIA cloud API

## 🔧 Files

```
├── Start.bat / Start.command   ← double-click to launch
├── requirements.txt
├── .env                        ← your API key (auto-created)
├── docs/                       ← drop your files here
├── rag/
│   ├── app.py                  ← Gradio web UI
│   ├── ingest.py               ← build vector DB
│   ├── query.py                ← CLI query
│   ├── watch.py                ← auto re-index on file change
│   └── embedder.py             ← NVIDIA embedding wrapper
├── chat.py                     ← terminal chat (no RAG)
└── chroma_db/                  ← vector DB (auto-created)
```

## 🔐 Privacy

- Your documents stay **local** — embeddings are computed via API but raw docs stay on disk
- Chat history is **in-memory only** (lost when you close the browser)
- To fully revoke: `docs/` + `chroma_db/` + `.env` → delete

## 🆘 Troubleshooting

| Problem | Fix |
|---|---|
| `python not found` | Install Python, check "Add to PATH" |
| `401 Unauthorized` | Regenerate API key at build.nvidia.com, update `.env` |
| Chinese shows as `???` | Already handled — the launcher sets UTF-8 |
| Port 7860 in use | Edit `rag/app.py` last line: `demo.launch(server_port=7861)` |

## 📜 License

MIT — remix freely.
