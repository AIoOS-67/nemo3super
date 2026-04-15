"""Ingest docs from ../docs/ into Chroma. Supports .txt, .md, .pdf."""
import sys
from pathlib import Path
import chromadb
from pypdf import PdfReader
from docx import Document
from embedder import embed

ROOT = Path(__file__).parent.parent
DOCS_DIR = ROOT / "docs"
DB_DIR = ROOT / "chroma_db"
CHUNK_SIZE = 400
CHUNK_OVERLAP = 60


def read_file(path: Path) -> str:
    suf = path.suffix.lower()
    if suf == ".pdf":
        return "\n".join(p.extract_text() or "" for p in PdfReader(path).pages)
    if suf == ".docx":
        doc = Document(str(path))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    return path.read_text(encoding="utf-8", errors="ignore")


def chunk(text: str) -> list[str]:
    chunks = []
    i = 0
    while i < len(text):
        chunks.append(text[i : i + CHUNK_SIZE])
        i += CHUNK_SIZE - CHUNK_OVERLAP
    return [c.strip() for c in chunks if c.strip()]


def main():
    DOCS_DIR.mkdir(exist_ok=True)
    exts = {".txt", ".md", ".pdf", ".py", ".json", ".html", ".docx"}
    skip_dirs = {".venv", "venv", "node_modules", "__pycache__", ".git",
                 "site-packages", "dist-info", ".pytest_cache"}
    files = [
        p for p in DOCS_DIR.rglob("*")
        if p.suffix.lower() in exts
        and not any(part in skip_dirs for part in p.parts)
    ]
    print(f"发现 {len(files)} 个文件\n")
    if not files:
        print(f"⚠️  没有文档。把 .txt/.md/.pdf 丢进 {DOCS_DIR} 再运行。")
        return

    client = chromadb.PersistentClient(path=str(DB_DIR))
    col = client.get_or_create_collection("knowledge_base")

    for f in files:
        print(f"📄 {f.relative_to(ROOT)}")
        text = read_file(f)
        chunks = chunk(text)
        if not chunks:
            continue
        # batch embed (NVIDIA API supports batches, cap at 50 for safety)
        for b in range(0, len(chunks), 50):
            batch = chunks[b : b + 50]
            vecs = embed(batch, input_type="passage")
            ids = [f"{f.name}::{b+i}" for i in range(len(batch))]
            col.upsert(ids=ids, documents=batch, embeddings=vecs,
                       metadatas=[{"source": str(f.name)}] * len(batch))
        print(f"   ✅ {len(chunks)} chunks")
    print(f"\n总计 collection 条数: {col.count()}")


if __name__ == "__main__":
    main()
