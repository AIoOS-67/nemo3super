"""Watch docs/ — auto-ingest new/modified files. Run: python watch.py"""
import time
from pathlib import Path
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import chromadb
from embedder import embed
from ingest import read_file, chunk

ROOT = Path(__file__).parent.parent
DOCS_DIR = ROOT / "docs"
DB_DIR = ROOT / "chroma_db"
EXTS = {".txt", ".md", ".pdf", ".py", ".json", ".html", ".htm",
        ".docx", ".xlsx", ".csv", ".pptx"}
SKIP = {".venv", "venv", "node_modules", "__pycache__", ".git",
        "site-packages", "dist-info", ".pytest_cache"}


def should_skip(path: Path) -> bool:
    return (
        path.suffix.lower() not in EXTS
        or any(part in SKIP for part in path.parts)
        or not path.is_file()
    )


def reindex_file(path: Path):
    col = chromadb.PersistentClient(path=str(DB_DIR)).get_or_create_collection("knowledge_base")
    try:
        text = read_file(path)
    except Exception as e:
        print(f"   [error] read failed: {e}")
        return
    chunks = chunk(text)
    if not chunks:
        return
    # remove old chunks for this file
    try:
        col.delete(where={"source": path.name})
    except Exception:
        pass
    for b in range(0, len(chunks), 50):
        batch = chunks[b : b + 50]
        vecs = embed(batch, input_type="passage")
        ids = [f"{path.name}::{b+i}::{int(time.time())}" for i in range(len(batch))]
        col.upsert(ids=ids, documents=batch, embeddings=vecs,
                   metadatas=[{"source": path.name}] * len(batch))
    print(f"   ✅ {len(chunks)} chunks")


class Handler(FileSystemEventHandler):
    def __init__(self):
        self.debounce = {}

    def _trigger(self, path_str: str):
        p = Path(path_str)
        if should_skip(p):
            return
        now = time.time()
        if now - self.debounce.get(path_str, 0) < 2:
            return
        self.debounce[path_str] = now
        print(f"📄 {p.relative_to(ROOT)}")
        reindex_file(p)

    def on_modified(self, e):
        if not e.is_directory:
            self._trigger(e.src_path)

    def on_created(self, e):
        if not e.is_directory:
            self._trigger(e.src_path)


def main():
    DOCS_DIR.mkdir(exist_ok=True)
    obs = Observer()
    obs.schedule(Handler(), str(DOCS_DIR), recursive=True)
    obs.start()
    print(f"Watching {DOCS_DIR}")
    print("   (Ctrl+C to stop. New/modified files are auto re-indexed.)")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        obs.stop()
    obs.join()


if __name__ == "__main__":
    main()
