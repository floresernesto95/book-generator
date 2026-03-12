import os
import subprocess
import re
import json

# Configuration
INPUT_DIR = 'book_sections'
EPUB_OUTPUT = 'final_book.epub'
TITLE_AND_SUBTITLE_FILEPATH = 'title_and_subtitle.txt'

# Load the title and subtitle data
with open(TITLE_AND_SUBTITLE_FILEPATH, 'r', encoding='utf-8') as f:
    title_and_subtitle = json.load(f)

title = title_and_subtitle['titulo']
subtitle = title_and_subtitle['subtitulo']

# List all markdown files in the input directory
all_files = os.listdir(INPUT_DIR)
    
# Sort files numerically
all_files.sort(key=lambda x: int(re.search(r'\d+', x).group()))

# Create complete paths
file_paths = [os.path.join(INPUT_DIR, f) for f in all_files]

# Build pandoc terminal command
pandoc_cmd = [
        'pandoc',
        *file_paths,
        '-o', EPUB_OUTPUT,
        '--toc',
        '--metadata', f'title={title}',
        '--metadata', f'subtitle={subtitle}',
        '--metadata', 'author=Don Flores',
        '--metadata', 'lang=es-ES'
    ]

# Execute pandoc command
subprocess.run(pandoc_cmd, check=True)
print(f"Successfully generated {EPUB_OUTPUT}")
    