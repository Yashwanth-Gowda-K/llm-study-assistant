import os
import json
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import SYSTEM_PROMPT
from retriever import retrieve_context

# Load the API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing")

# Create the Gemini client
client = genai.Client(api_key=api_key)

# Define the JSON response structure
response_schema = {
    "type": "OBJECT",
    "properties": {
        "definition": {"type": "STRING"},
        "example": {"type": "STRING"},
        "key_takeaway": {"type": "STRING"}
    },
    "required": ["definition", "example", "key_takeaway"]
}

# Give Gemini clear rules for answering from retrieved notes
rag_system_prompt = SYSTEM_PROMPT + """
You are answering questions using retrieved study notes.
Use the supplied context as your primary source.
If the context does not contain the answer, say that the notes
do not contain enough information. Do not invent facts.
Keep the answer simple and concise.
"""

# Create a chat session
chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction=rag_system_prompt,
        response_mime_type="application/json",
        response_schema=response_schema
    )
)

# Ask questions until the user types exit
while True:
    question = input("\nYou: ").strip()

    if question.lower() == "exit":
        break

    if not question:
        continue

    try:
        # Retrieve relevant paragraphs from your notes
        context = retrieve_context(question)
        print("\n--- RETRIEVED CONTEXT ---")
        print(context or "No matching information found.")
        print("-------------------------")

        if not context:
            print("\nNo matching information found in your notes.")
            continue

        # Combine retrieved context and the user's question
        rag_message = f"""
RETRIEVED CONTEXT:
{context}

USER QUESTION:
{question}

Answer using the retrieved context.
"""

        # Retry temporary Gemini server errors up to 3 times
        response = None

        for attempt in range(3):
            try:
                response = chat.send_message(rag_message)
                break
            except Exception as error:
                if "503" in str(error) and attempt < 2:
                    print("Gemini is busy. Retrying in 2 seconds...")
                    time.sleep(2)
                else:
                    raise

        if response is None:
            print("Gemini is temporarily unavailable. Try again later.")
            continue

        # Convert JSON into a Python dictionary
        result = json.loads(response.text)

        # Display the answer
        print("\nDEFINITION:", result["definition"])
        print("\nEXAMPLE:", result["example"])
        print("\nKEY TAKEAWAY:", result["key_takeaway"])

    except (ValueError, KeyError, TypeError) as error:
        print("Could not process the response:", error)

    except Exception as error:
        print("Something went wrong:", error)