# PDF to Word Converter Backend

A FastAPI backend for converting PDF files to Word documents.

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the server

```bash
python run.py
```

This will start the server at http://localhost:8000

## API Endpoints

- `GET /`: Welcome message
- `POST /convert`: Convert PDF to Word
  - Expects: multipart/form-data with a file field
  - Returns: The converted Word document

## Development

The server runs with hot-reload enabled, so any changes to the code will automatically restart the server.
