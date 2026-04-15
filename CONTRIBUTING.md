# Contributing to Nemotron-RAG

Thanks for your interest! This is an intentionally small, readable project — the goal is that any
developer can grok the whole thing in 30 minutes.

## 🐛 Reporting Bugs

Open a [GitHub issue](../../issues/new) with:
- OS + Python version (`python --version`)
- The failing command and the full error trace
- What you expected vs. what happened

## 💡 Feature Ideas

Check the [Roadmap](RELEASE_NOTES.md#-roadmap) first — if it's not there, open an issue with
the "enhancement" label so we can discuss scope before a PR.

## 🔧 Dev Setup

```bash
git clone <your-fork>
cd nemotron-rag
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in your NVIDIA_API_KEY
```

Run the smoke test first:

```bash
python test_nemotron.py
```

If that prints a real answer, the API layer works. Then test the RAG stack:

```bash
# put at least one file in docs/
python rag/ingest.py
python rag/query.py "hello"
python rag/app.py
```

## 🧹 Style Guide

- **No frameworks if a stdlib can do it.** This project favors clarity over abstraction.
- **No new deps without a good reason.** Every `pip install` is paid for by the user's first launch.
- **Keep `rag/` files under ~150 lines each.** If one grows larger, split it.
- **Comments explain *why*, not *what*.** Function names should do the "what" work.
- **UTF-8 everywhere.** Don't let Chinese filenames or Chinese content break tooling.

## 🧪 Testing a Change

Before opening a PR, run through this manually:

1. `python test_nemotron.py` — API still works
2. `python rag/ingest.py` — ingests the sample doc without errors
3. `python rag/query.py "What do you think of Tesla's IPO?"` — returns a grounded answer with a source citation
4. `python rag/app.py` — UI launches, both example prompts work
5. `python build_portable.py` — zip builds under 20 KB

## 📦 Pull Requests

- One logical change per PR
- Keep the diff small — 200 lines or less is ideal
- Update `RELEASE_NOTES.md` if your change is user-facing
- No auto-generated commits, no `fix typo` churn — squash locally first

## 📜 License

By contributing, you agree your code is released under the MIT license.
