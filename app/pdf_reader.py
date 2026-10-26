
from pathlib import Path
from pypdf import PdfReader


def read_pdf(pdf_path: str) -> str:
    """Extract text from a PDF file."""

    path = Path(pdf_path)

    # Check whether the PDF exists
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")

    # Open the PDF
    reader = PdfReader(str(path))

    # Extract text from every page
    pages = []

    for page in reader.pages:
        text = page.extract_text() or ""

        if text.strip():
            pages.append(text.strip())

    # Combine all pages into one string
    return "\n\n".join(pages)
