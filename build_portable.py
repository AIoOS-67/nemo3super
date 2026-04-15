"""Build a portable zip distribution. Run: python build_portable.py"""
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).parent
import time
DIST = ROOT / "dist"
STAGE = DIST / f"_stage_{int(time.time())}"
ZIP_PATH = DIST / "Nemotron-RAG.zip"

# Files/dirs to include in the portable package
INCLUDE_FILES = [
    "requirements.txt",
    ".env.example",
    ".gitignore",
    "chat.py",
    "test_nemotron.py",
]
INCLUDE_DIRS = ["rag"]
# Sample doc shipped so first-run users can immediately try a query
SAMPLE_DOC = "docs/sample_tesla_ipo.md"


def main():
    if STAGE.exists():
        shutil.rmtree(STAGE)
    STAGE.mkdir(parents=True)

    for f in INCLUDE_FILES:
        src = ROOT / f
        if src.exists():
            shutil.copy2(src, STAGE / f)
            print(f"  + {f}")

    for d in INCLUDE_DIRS:
        src = ROOT / d
        if src.exists():
            shutil.copytree(
                src, STAGE / d,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
            )
            print(f"  + {d}/")

    (STAGE / "docs").mkdir()
    sample = ROOT / SAMPLE_DOC
    if sample.exists():
        shutil.copy2(sample, STAGE / SAMPLE_DOC)
        print(f"  + {SAMPLE_DOC}")

    for launcher in ["Start.bat", "Start.command", "README.md"]:
        src = DIST / launcher
        if src.exists():
            shutil.copy2(src, STAGE / launcher)
            print(f"  + {launcher}")

    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for p in STAGE.rglob("*"):
            if p.is_file():
                arc = Path("Nemotron-RAG") / p.relative_to(STAGE)
                zf.write(p, arc)

    size_mb = ZIP_PATH.stat().st_size / 1024 / 1024
    print(f"\n[OK] Built: {ZIP_PATH}  ({size_mb:.1f} MB)")
    print(f"[Staged] {STAGE}")
    print("\nReady to upload to GitHub Release.")


if __name__ == "__main__":
    main()
