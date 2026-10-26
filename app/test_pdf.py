from pathlib import Path
from pdf_reader import read_pdf

pdf_path = Path(__file__).resolve().parent.parent / "documents" / "sample.pdf"

text = read_pdf(str(pdf_path))

print(text[:2000])