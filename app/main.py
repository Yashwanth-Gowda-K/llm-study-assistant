import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import SYSTEM_PROMPT, USER_PROMPT

# Load .env
load_dotenv()
username = input("Enter your name: ")
name = (username)
# Get API key
api_key = os.getenv("GEMINI_API_KEY")

# Stop immediately if the key is missing
if not api_key:
    raise ValueError("GEMINI_API_KEY is missing")

# Create Gemini client
client = genai.Client(api_key=api_key)
while True:
    topic = input("\nYou: ")
    if topic.strip().lower() in ('exit', 'q'):
        print(f"It was nice talking talking to you: {name}")
        break

    prompt = USER_PROMPT.format(topic=topic)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
        response_mime_type="application/json",
        response_schema={
            "type": "OBJECT",
            "properties": {
                "definition": {
                    "type": "STRING"
                },
                "example": {
                    "type": "STRING"
                },
                "key_takeaway": {
                    "type": "STRING"
                }
            },
            "required": [
                "definition",
                "example",
                "key_takeaway"
            ]
        }
        )
    )


    result = json.loads(response.text)

    print("\nDefinition:", result["definition"])
    print("\nExample:", result["example"])
    print("\nKey Takeaway:", result["key_takeaway"])
