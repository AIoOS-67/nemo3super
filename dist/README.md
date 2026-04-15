# 🧠 Nemotron 3 Super × Your Private Knowledge Base

A zero-config, private RAG chatbot powered by **NVIDIA Nemotron 3 Super 120B**.
Drop your docs into `docs/`, chat with them in the browser — your data never leaves your machine (except the LLM call to NVIDIA's API).

## 🚀 Quick Start

### Windows
1. **Install Python 3.10+** from https://python.org (check "Add to PATH" during install)
2. **Get a free NVIDIA API key** at https://build.nvidia.com (Sign up → model page → "Get API Key")
3. **Double-click `Start.bat`**

> ⚠️ **"Unknown Publisher" warning on first launch?** That's expected —
> the script isn't code-signed (a $200-500/yr certificate we don't buy for a free
> project). Click **Run** to proceed. To silence it permanently:
> right-click `Start.bat` → **Properties** → tick **Unblock** at the bottom → OK.
> The script is plain text — open it in Notepad first if you want to verify it's safe.
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

Drop files into the `docs/` folder. Supported formats:

| Category | Extensions |
|---|---|
| Documents | `.pdf` `.docx` `.md` `.txt` |
| Spreadsheets | `.xlsx` `.csv` |
| Slides | `.pptx` |
| Code / config | `.py` `.json` `.html` |

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
| "Unknown Publisher" security warning | Expected — click Run, or right-click → Properties → Unblock |
| `401 Unauthorized` | Regenerate API key at build.nvidia.com, update `.env` |
| Chinese shows as `???` | Already handled — the launcher sets UTF-8 |
| Port 7860 in use | Edit `rag/app.py` last line: `demo.launch(server_port=7861)` |

## 📜 License

MIT — remix freely.
