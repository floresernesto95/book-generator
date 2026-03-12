from google import genai
from google.genai import types
import os
import json

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL_NAME = "gemini-2.5-flash"
PROMPT_FILEPATH = 'prompt_outline_generator.txt'
TITLE_AND_SUBTITLE_FILEPATH = 'title_and_subtitle.txt'

# Initialize client
client = genai.Client(api_key=GEMINI_API_KEY)

# Read prompt from file
with open(PROMPT_FILEPATH, 'r', encoding='utf-8') as f:
    prompt = f.read()
    
# Load the title and subtitle data
with open(TITLE_AND_SUBTITLE_FILEPATH, 'r', encoding='utf-8') as f:
    title_and_subtitle = json.load(f)
  
# Format the prompt with the title and subtitle    
title = title_and_subtitle['titulo']
subtitle = title_and_subtitle['subtitulo']

prompt = prompt.format(titulo=title, subtitulo=subtitle)

# Generate response
response = client.models.generate_content(
    model=GEMINI_MODEL_NAME,
    contents=prompt,
    config=types.GenerateContentConfig(
        temperature=1.0,
        max_output_tokens=65536,
        response_mime_type="application/json"
    )
)

# Print the response
print(response.text)

# Save the response to a file    
with open("outline.txt", "w", encoding="utf-8") as f:
    f.write(response.text)