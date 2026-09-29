import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import SYSTEM_PROMPT

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini_API_KEY is missing")

client = genai.Client(api_key=api_key)

response_schema = {
    "type":"object",
    "properties":{
        "definition": {"type":"STRING"},
        "example":{"type":"STRING"},
        "key_takeaway":{"type":"STRING"}
    },
    "required":["definition","example","key_takeaway"]
}
chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        response_mime_type="application/json",
        response_schema=response_schema
    )
)
while True:
    question = input("\nYou: ").strip()

    if question.lower() == "exit":
        break

    if not question:
        continue

    try:
        response = chat.send_message(question)
        result = json.loads(response.text)
        print("\nDEFINITION:", result["definition"])
        print("\nEXAMPLE:", result["example"])
        print("\nKEY TAKEAWAY:", result["key_takeaway"])

    except (ValueError, KeyError, TypeError) as error:
        print("Could not process the response:", error)

    except Exception as error:
        print("Something went wrong:", error)