import os

from dotenv import load_dotenv
from google import genai
from prompts import STUDY_PROMPT

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
    short = ("Explain me everything in simple and shorter with the rules i dont want to expload my head... and use emojs also , dont make the learning boaring make it instersting..")
    prompt = short + STUDY_PROMPT.format(topic=topic)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    print("\nAI --> " ,response.text)