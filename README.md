# Vector Search CLI

A completely local, command-line based semantic search engine for your personal notes. 

This project uses [Qdrant](https://qdrant.tech/) as a local vector database and [SentenceTransformers](https://sbert.net/) (specifically `all-MiniLM-L6-v2`) to generate embeddings. It allows you to search through your text files based on meaning and context rather than exact keyword matches.

## Features

- **100% Local**: No API keys required. All embeddings and vector storage happen on your machine.
- **Semantic Search**: Understands the context of your queries to find the most relevant notes.
- **Chunking**: Automatically splits your notes into chunks (separated by double newlines) for granular search results.
- **Source Tracking**: Search results include the source file name, confidence score, and the exact matched text.

## Prerequisites

- Python 3.8 or higher

## Installation

1. Clone this repository or download the source code.
2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```
3. Install the required dependencies:
   ```bash
   pip install qdrant-client sentence-transformers
   ```

## Usage

### 1. Add your notes
Place your text files (`.txt`) in the `notes/` directory. If the directory doesn't exist, create it in the project root. 

> **Tip**: The ingestion script separates chunks by double newlines (`\n\n`). For best results, format your notes into bite-sized paragraphs.

### 2. Ingest your notes
Run the ingestion script to process your notes, generate vector embeddings, and store them in the local Qdrant database (saved in `./qdrant_db`).

```bash
python ingest.py
```

### 3. Search your notes
Run the search script to launch the interactive search CLI.

```bash
python search.py
```

- Enter your search query when prompted.
- The system will return the top 3 most relevant chunks along with their confidence scores and source files.
- Type `exit` to quit the program.

## Project Structure

- `ingest.py`: Reads text files from the `notes/` directory, chunks them, generates vector embeddings, and upserts them into Qdrant.
- `search.py`: Command-line interface to encode your search query and retrieve the top matches from Qdrant.
- `notes/`: Directory where your input `.txt` files should be placed.
- `qdrant_db/`: Automatically generated directory where the local vector database is stored.