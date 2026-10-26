from pathlib import Path
from pdf_reader import read_pdf
from chunking import split_text

# Find the PDF
pdf_path = Path(__file__).resolve().parent.parent / "documents" / "sample.pdf"

# Extract the PDF text
text = read_pdf(str(pdf_path))

# Split the text into chunks
chunks = split_text(text)

# Display the results
print("Total chunks:", len(chunks))
print("\nFirst chunk:\n", chunks[0] if chunks else "No text found")