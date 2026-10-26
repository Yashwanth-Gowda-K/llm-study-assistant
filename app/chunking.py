
def split_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Split text into small chunks with overlapping text."""

    text = " ".join(text.split())
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks
