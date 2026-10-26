
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

from retriever import retrieve_context


# Load the API key
PROJECT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_DIR / ".env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from .env")

# Create the Gemini client
client = genai.Client(api_key=api_key)


def answer_question(question: str) -> str:
    """Answer a question using retrieved information."""

    # Retrieve relevant information
    context = retrieve_context(question, top_k=3)

    if not context:
        return "I couldn't find relevant information in your notes or PDF."

    # Tell Gemini to answer using only the retrieved information
    prompt = f"""
  Answer the question using ONLY the context below.
If the context does not contain the answer, say you don't know.
Explain in simple English using 2-4 sentences.
Include the important details from the context.
    {context}

    Question:
    {question}

    Answer:
    """

    # Generate the answer
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text or "I couldn't generate an answer."


if __name__ == "__main__":
    question = input("Ask a question: ")
    answer = answer_question(question)

    print("\n--- GENERATED ANSWER ---")
    print(answer)
