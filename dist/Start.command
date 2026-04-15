#!/bin/bash
# macOS / Linux launcher
cd "$(dirname "$0")"

echo "============================================================"
echo "  Nemotron 3 Super x Your Private Knowledge Base"
echo "============================================================"

if ! command -v python3 &> /dev/null; then
  echo "[Error] Python 3 not found. Install from https://python.org"
  exit 1
fi

if [ ! -d ".venv" ]; then
  echo "[First launch] Creating venv + installing dependencies..."
  python3 -m venv .venv
  source .venv/bin/activate
  pip install --upgrade pip -q
  pip install -r requirements.txt -q
else
  source .venv/bin/activate
fi

if [ ! -f ".env" ]; then
  read -p "NVIDIA_API_KEY: " NVKEY
  echo "NVIDIA_API_KEY=$NVKEY" > .env
fi

if [ ! -d "chroma_db" ] && [ -n "$(ls -A docs 2>/dev/null)" ]; then
  echo "[Indexing] first-time build..."
  (cd rag && python ingest.py)
fi

echo "[Launching] Open browser when ready."
cd rag && python app.py
