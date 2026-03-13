# 📖 Book generator

An end-to-end automated pipeline designed to conceptualize, write, and assemble complete books using Generative Artificial Intelligence. This project leverages prompt engineering, context management, and document conversion to transform a simple subject idea into a fully structured, continuous, and professionally formatted EPUB electronic book without manual intervention.

## 🚀 Main features

* **Modular generation pipeline:** Decoupled architecture that sequentially handles title creation, structural outlining, chapter drafting, and final compilation.
* **Context-aware writing:** Implements a dynamic context accumulator that feeds previously generated sections into the AI for subsequent chapters, ensuring narrative continuity and logical flow.
* **Smart validation and retries:** Built-in verification mechanisms to ensure generated chapters meet minimum word count requirements, automatically re-prompting the AI up to a maximum number of attempts if it falls short.
* **Strict structural formatting:** Utilizes JSON schema enforcement within prompt instructions to guarantee parseable, structured responses for outlines and metadata.
* **Automated document assembly:** Integration with Pandoc via system subprocesses to automatically compile multiple Markdown files into a standardized EPUB format with localized metadata and table of contents.

## 🛠️ Technology stack

This project demonstrates strong competencies in backend orchestration and AI integration:

* **Language:** Python 3
* **AI integration:** Google GenAI SDK (Gemini 2.5 Flash model)
* **Document compilation:** Pandoc (markdown to EPUB conversion)
* **Standard libraries:** `json`, `os`, `re`, `subprocess`
* **Prompt engineering:** Advanced prompt templates with variable injection for precise AI control

## ⚙️ Workflow architecture

The system operates through a sequential, four-stage pipeline:

1. **Conceptualization (`title_and_subtitle_generator.py`):** * Takes a base subject and queries the Gemini API to output a catchy title and subtitle in a strictly formatted JSON file.
2. **Structuring (`outline_generator.py`):** * Uses the generated title to create a comprehensive book outline, breaking the content into primary sections and specific topics, saved as JSON.
3. **Drafting (`book_generator.py`):** * Iterates through the structured outline.
* Feeds the AI the current section requirements alongside the accumulated text of all previous sections.
* Validates word count targets and retries if necessary.
* Saves each section as sequentially numbered Markdown files.


4. **Assembly (`book_assembler.py`):** * Reads the generated Markdown chapters and metadata.
* Orchestrates a Pandoc subprocess command to compile the files into a final `final_book.epub`.



## 📋 Prerequisites

To run this project locally, you need an Ubuntu or similar Linux environment with the following installed:

1. **Python 3.8+**
2. **Pandoc** installed on your system (`sudo apt install pandoc`)
3. Environment variables configured:
* `GEMINI_API_KEY`: Your Google AI Studio API key



### Dependency installation

```bash
pip install google-genai

```

## 📂 Project structure

```text
├── .env                        # Environment variables
├── prompts/                    # AI prompt engineering templates
│   ├── prompt_book_generator.txt
│   ├── prompt_outline_generator.txt
│   └── prompt_title_and_subtitle_generator.txt
├── src/                        # Source code
│   ├── book_assembler.py       # Compiles MD to EPUB
│   ├── book_generator.py       # Generates chapter content
│   ├── outline_generator.py    # Creates the JSON outline
│   └── title_and_subtitle_generator.py
└── README.md                   # Project documentation

```

## 💡 Overcome challenges and learnings

During the development of this pipeline, several technical hurdles were resolved:

* **Context window management:** To prevent the AI from losing track of the book's narrative, a rolling context window was implemented. The system reads the saved markdown files of previous chapters and injects them into the prompt, guaranteeing smooth transitions.
* **Handling AI unreliability:** LLMs can occasionally produce shorter text than requested. I implemented a robust `while` loop with a maximum attempt counter that validates the output word count against the outline's minimum requirement, retrying the generation automatically if it fails.
* **Consistent data parsing:** Extracting structured data from LLMs can be tricky. By enforcing strict JSON formatting rules in the system prompts and configuring the response MIME type in the SDK, the system guarantees clean data for the Python scripts to parse.

## 🔮 Future improvements

* Implementation of asynchronous generation (`asyncio`) to write independent sub-chapters concurrently and reduce overall execution time.
* Integration with a PDF generation library for alternative export formats.
* A command-line interface (CLI) to allow users to input parameters (subject, target length, author name) dynamically without modifying the code.
