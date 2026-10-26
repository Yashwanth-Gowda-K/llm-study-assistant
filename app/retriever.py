
import os
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from google import genai
from google.genai import types


# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_FILE = PROJECT_DIR / "data" / "rag_notes.txt"
DB_DIR = PROJECT_DIR / "data" / "chroma_db"


# --------------------------------------------------
# 2. Load Gemini API key
# --------------------------------------------------

load_dotenv(PROJECT_DIR / ".env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=api_key)


# --------------------------------------------------
# 3. Connect to ChromaDB
# --------------------------------------------------

chroma_client = chromadb.PersistentClient(path=str(DB_DIR))

collection = chroma_client.get_or_create_collection(
    name="study_notes"
)


# --------------------------------------------------
# 4. Create embeddings
# --------------------------------------------------

def create_embedding(text: str, task_type: str) -> list[float]:
    """Convert text into a numerical vector."""

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config=types.EmbedContentConfig(
            task_type=task_type
        ),
    )

    return response.embeddings[0].values


# --------------------------------------------------
# 5. Index existing text notes
# --------------------------------------------------

def index_documents():
    """Index paragraphs from rag_notes.txt."""

    if not KNOWLEDGE_FILE.exists():
        print("Notes file not found. Skipping notes indexing.")
        return

    text = KNOWLEDGE_FILE.read_text(encoding="utf-8")

    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    file_id = str(KNOWLEDGE_FILE.resolve())

    stored = collection.get(
        where={"file_id": file_id},
        include=["metadatas"],
    )

    existing_texts = {
        metadata["text"]
        for metadata in stored["metadatas"]
        if metadata and "text" in metadata
    }

    new_paragraphs = [
        paragraph
        for paragraph in paragraphs
        if paragraph not in existing_texts
    ]

    if new_paragraphs:
        embeddings = [
            create_embedding(
                paragraph,
                "RETRIEVAL_DOCUMENT",
            )
            for paragraph in new_paragraphs
        ]

        ids = [
            f"{file_id}::{i}"
            for i in range(len(new_paragraphs))
        ]

        collection.upsert(
            ids=ids,
            documents=new_paragraphs,
            embeddings=embeddings,
            metadatas=[
                {
                    "file_id": file_id,
                    "text": paragraph,
                }
                for paragraph in new_paragraphs
            ],
        )

        print(f"Indexed {len(new_paragraphs)} new note paragraphs.")
    else:
        print("Notes are already indexed.")

    # Remove outdated note paragraphs
    current_texts = set(paragraphs)

    outdated_ids = [
        item_id
        for item_id, metadata in zip(
            stored["ids"],
            stored["metadatas"],
        )
        if metadata and metadata.get("text") not in current_texts
    ]

    if outdated_ids:
        collection.delete(ids=outdated_ids)
        print(f"Removed {len(outdated_ids)} outdated note paragraphs.")


# --------------------------------------------------
# 6. Normalize words for keyword matching
# --------------------------------------------------

def normalize(word: str) -> str:
    """Treat selected word forms as equivalent."""

    word = word.lower().strip("?!.,:;()[]{}\"'")

    word_groups = {
        "retrieve": [
            "retrieve",
            "retrieves",
            "retrieved",
            "retrieving",
            "retrieval",
        ],
        "answer": [
            "answer",
            "answers",
            "answered",
            "answering",
        ],
        "embed": [
            "embed",
            "embeds",
            "embedded",
            "embedding",
            "embeddings",
        ],
    }

    for base, forms in word_groups.items():
        if word in forms:
            return base

    return word


# --------------------------------------------------
# 7. Retrieve relevant text from notes and PDFs
# --------------------------------------------------

def retrieve_context(question: str, top_k: int = 3) -> str:
    """Find relevant chunks across all indexed sources."""

    # Index or update the existing notes
    index_documents()

    # Check whether ChromaDB contains anything
    total_documents = collection.count()

    if total_documents == 0:
        print("No documents found in ChromaDB.")
        return ""

    # Convert the question into an embedding
    query_embedding = create_embedding(
        question,
        "RETRIEVAL_QUERY",
    )

    # Search across notes and PDF chunks
    candidate_count = min(10, total_documents)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=candidate_count,
        include=["documents", "distances"],
    )

    documents = results["documents"][0] if results["documents"] else []
    distances = results["distances"][0] if results["distances"] else []

    if not documents:
        print("No documents matched the search.")
        return ""

    # Ignore common words when comparing keywords
    stop_words = {
        "how", "does", "do", "is", "are", "the", "a", "an",
        "what", "why", "when", "where", "to", "of", "in",
        "on", "and", "or", "it", "with", "for", "can", "rag",
    }

    question_words = {
        normalize(word) for word in question.split()
    } - stop_words

    # Combine semantic similarity and keyword overlap
    reranked = []

    for document, distance in zip(documents, distances):
        document_words = {
            normalize(word) for word in document.split()
        }

        overlap = len(question_words & document_words)

        keyword_score = overlap / max(len(question_words), 1)

        semantic_score = 1 / (1 + distance)

        final_score = (
            0.7 * semantic_score
            + 0.3 * keyword_score
        )

        reranked.append(
            (final_score, document, distance)
        )

    # Best matches first
    reranked.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    # Reject low-scoring matches
    MIN_SCORE = 0.45

    selected = [
        item
        for item in reranked
        if item[0] >= MIN_SCORE
    ][:max(1, top_k)]

    if not selected:
        print("No sufficiently relevant text found.")
        return ""

    # Display selected results
    print("\n--- RETRIEVED RESULTS ---")

    for score, document, distance in selected:
        print(f"\nScore: {score:.4f}")
        print(document)

    # Return context for the LLM
    return "\n\n".join(
        document
        for score, document, distance in selected
    )
