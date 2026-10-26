"""Extract text from a PDF for manual normalization into venues.json."""
from pathlib import Path
from pypdf import PdfReader
PDF = Path(__file__).resolve().parent / "data" / "venues.pdf"
OUT = Path(__file__).resolve().parent / "data" / "venues_extracted.txt"

def main():
    if not PDF.exists():
        raise FileNotFoundError(f"Put the source PDF at: {PDF}")
    reader = PdfReader(str(PDF))
    chunks = []
    for i, page in enumerate(reader.pages, start=1):
        chunks.append(f"\n===== PAGE {i} =====\n{page.extract_text() or ''}")
    OUT.write_text("\n".join(chunks), encoding="utf-8")
    print(f"Extracted {len(reader.pages)} pages to {OUT}")
    print("Review the text and manually normalize each venue into venues.json.")

if __name__ == "__main__":
    main()
