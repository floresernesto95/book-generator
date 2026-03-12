# AI-powered automated book generator 📖

A fully automated, modular pipeline that generates complete, cohesive books from a single subject prompt using the Google Gemini API. The system handles everything from brainstorming the title to compiling the final `.epub` file, ensuring narrative continuity and structural integrity throughout the generation process.

## Project overview 🎯

This project demonstrates advanced API integration, prompt engineering, and automated workflow orchestration. It breaks down the complex task of writing a book into manageable, programmatic steps. By maintaining the context of previously generated chapters, the system ensures a logical flow and avoids repetitive content, simulating a ghostwriter's process.

## Key features ✨

* **Modular architecture:** The project is separated into distinct, single-responsibility scripts (title generation, outlining, content drafting, and assembling).
* **Context-aware generation:** The content generator feeds previously written sections into the LLM's prompt context to maintain continuity.
* **Quality assurance loop:** Includes a retry mechanism that automatically regenerates a section if the output does not meet the strict minimum word count requirement.
* **Dynamic prompting:** Externalized prompt templates (`.txt` files) allow for easy adjustments without modifying the core Python logic.
* **Automated compilation:** Uses Pandoc to stitch the generated markdown files together into a professionally formatted EPUB, complete with a table of contents and metadata.

## Tech stack and tools 🛠️

* **Language:** Python 3
* **AI/LLM:** Google Gemini API (`gemini-2.5-flash` model)
* **Data formatting:** JSON handling for structured prompt responses
* **Document conversion:** Pandoc
* **OS compatibility:** Developed and tested on Ubuntu/Linux 🐧

## Pipeline architecture ⚙️

The system runs sequentially through four main stages:

1. **`title_and_subtitle_generator.py`:** Takes a base subject and prompts Gemini to return a catchy title and subtitle in a structured JSON format.
2. **`outline_generator.py`:** Consumes the generated title/subtitle and outputs a deeply structured JSON outline, detailing primary sections and target word counts.
3. **`book_generator.py`:** The core engine. It iterates through the JSON outline, utilizing the `prompt_book_generator.txt` template. It manages API calls, verifies length requirements, and saves each chapter sequentially in the `book_sections/` directory.
4. **`book_assembler.py`:** Reads the sorted markdown files and executes a terminal command to bind them into `final_book.epub` using Pandoc.

## Getting started on Ubuntu 🚀

Follow these steps to run the pipeline locally:

1. **Clone the repository:**
```bash
git clone <repository_url>
cd v0.0-multiple-parts-github
```


2. **Install dependencies:**
Ensure you have Python installed, then install the required Gemini SDK. You will also need to install Pandoc for the final assembly.
```bash
pip install google-genai
sudo apt-get update
sudo apt-get install pandoc
```


3. **Configure environment variables:**
Copy the `.env.example` file to create your own `.env` and add your Gemini API key.
```bash
cp .env.example .env
```


4. **Run the pipeline:**
Execute the scripts in order to generate your book.
```bash
python src/title_and_subtitle_generator.py
python src/outline_generator.py
python src/book_generator.py
python src/book_assembler.py
```