from retriever import retrieve_context

question = input("Ask a question about your PDF: ")

context = retrieve_context(question, top_k=3)

if context:
    print("\n--- RETRIEVED CONTEXT ---")
    print(context)
else:
    print("No relevant information found.")