from google import genai
from google.genai import types
import os
import json

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL_NAME = "gemini-2.5-flash"
PROMPT_FILEPATH = 'prompt_book_generator.txt'
TITLE_AND_SUBTITLE_FILEPATH = 'title_and_subtitle.txt'
OUTLINE_FILEPATH = 'outline.txt'
OUTPUT_DIR = 'book_sections'

# Initialize client
client = genai.Client(api_key=GEMINI_API_KEY)

# Ensure output directory exists
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Read prompt from file
with open(PROMPT_FILEPATH, 'r', encoding='utf-8') as f:
    prompt_template = f.read()
    
# Load the title, subtitle, and outline data
with open(TITLE_AND_SUBTITLE_FILEPATH, 'r', encoding='utf-8') as f:
    title_and_subtitle = json.load(f)
    
with open(OUTLINE_FILEPATH, 'r', encoding='utf-8') as f:
    outline = json.load(f)
    
title_and_subtitle = json.dumps(title_and_subtitle, indent=2, ensure_ascii=False)
outline = json.dumps(outline, indent=2, ensure_ascii=False)

# Initialize string to hold text from previous sections
accumulated_context = ""
    
# Loop through each main section in the outline data
for index, section in enumerate(outline["secciones_primarias"]):
    section_number = index + 1
    title = section["titulo"]
    minimum_words = int(section["palabras_minimas_objetivo"])   
    
    output_filename = os.path.join(OUTPUT_DIR, f"section_{section_number}.md") 
    
    # Check if the file for this section was already generated
    if os.path.exists(output_filename):
        print(f"Skipping {title}, the file already exists")
        with open(output_filename, 'r', encoding='utf-8') as f:
            accumulated_context += f.read()
        continue

    requirement_met = False
    attempts = 0
    max_attempts = 3
    
    # Keep trying until success or max attempts reached
    while not requirement_met and attempts < max_attempts:
        attempts += 1
        print(f"Generating {title}, attempt {attempts}")
                
        formatted_prompt = prompt_template.format(
            titulo_y_subtitulo=title_and_subtitle,
            esquema_general=outline,
            titulo_seccion=title,
            palabras_minimas=minimum_words,
            contexto_previo=accumulated_context
        )
                
        response = client.models.generate_content(
            model=GEMINI_MODEL_NAME,
            contents=formatted_prompt,
            config=types.GenerateContentConfig(
                temperature=1.0,
                max_output_tokens=65536,
            )
        )
    
        generated_text = response.text
        word_count = len(generated_text.split())
        
        # Check if the generated text is long enough
        if word_count >= minimum_words:
            requirement_met = True
            print(f"{title} generated successfully, words: {word_count}") 
            
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(generated_text) 
                
            accumulated_context += generated_text
        else:
            print(f"{title} did not meet the word requirement, words: {word_count}")      
        
# Check if the final section failed to generate after all attempts
if not requirement_met:
    print(f"Failed to generate {title} after {max_attempts} attempts")