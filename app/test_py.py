
from retriever import retrieve_context

# Test three different questions
questions = [
    "What are embeddings?",
    "How does RAG retrieve information?",
    "Why can RAG give incorrect answers?",
    "What is photosynthesis?"
]
# Test each question
for question in questions:
    print("\n" + "=" * 50)
    print("QUESTION:", question)

    # Retrieve the three most relevant paragraphs
    context = retrieve_context(question, top_k=3)

    print("\nRETRIEVED CONTEXT:")
    print(context)
