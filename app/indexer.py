
from pathlib import Path

from pdf_reader import read_pdf
from chunking import split_text
from retriever import create_embedding, collection


# Find the PDF
PROJECT_DIR = Path(__file__).resolve().parent.parent
PDF_PATH = PROJECT_DIR / "documents" / "sample.pdf"


def index_pdf():
    """Read a PDF, split it into chunks, and store them in ChromaDB."""

    # Stop if the PDF does not exist
    if not PDF_PATH.exists():
        raise FileNotFoundError(f"PDF not found: {PDF_PATH}")

    # Extract text from the PDF
    text = read_pdf(str(PDF_PATH))

    if not text.strip():
        raise ValueError("No text could be extracted from the PDF.")

    # Divide the text into smaller pieces
    chunks = split_text(text)

    # Create a unique ID for this PDF
    file_id = str(PDF_PATH.resolve())

    # Find previously indexed chunks from this PDF
    existing = collection.get(
        where={"file_id": file_id},
        include=["metadatas"],
    )

    existing_texts = {
        metadata["text"]
        for metadata in existing["metadatas"]
        if metadata and "text" in metadata
    }

    # Keep only chunks that are not already stored
    new_chunks = [
        chunk for chunk in chunks
        if chunk not in existing_texts
    ]

    # Convert chunks into embeddings and save them
    if new_chunks:
        embeddings = [
            create_embedding(chunk, "RETRIEVAL_DOCUMENT")
            for chunk in new_chunks
        ]

        ids = [
            f"{file_id}::{i}"
            for i in range(len(new_chunks))
        ]

        collection.upsert(
            ids=ids,
            documents=new_chunks,
            embeddings=embeddings,
            metadatas=[
                {"file_id": file_id, "text": chunk}
                for chunk in new_chunks
            ],
        )

        print(f"Successfully indexed {len(new_chunks)} new chunks.")
    else:
        print("PDF chunks are already indexed.")

    # Remove old chunks that are no longer present
    current_texts = set(chunks)

    outdated_ids = [
        item_id
        for item_id, metadata in zip(
            existing["ids"],
            existing["metadatas"],
        )
        if metadata and metadata.get("text") not in current_texts
    ]

    if outdated_ids:
        collection.delete(ids=outdated_ids)
        print(f"Removed {len(outdated_ids)} outdated chunks.")

    print(f"Total chunks in PDF: {len(chunks)}")


if __name__ == "__main__":
    index_pdf()
