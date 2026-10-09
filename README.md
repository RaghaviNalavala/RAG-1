# AI Coding Assistant — Learn, Debug, Practice, and Master Programming with RAG

A complete local-first AI coding assistant built with a Python FastAPI backend, a React + Vite + TypeScript frontend, Ollama for local LLMs, and ChromaDB for vector search. The project uses qwen2.5:3b as the default generation model and nomic-embed-text as the local embedding model.

## Project overview

This project demonstrates a working Retrieval-Augmented Generation (RAG) workflow for programming assistance:

- Ask coding questions grounded in local knowledge-base files
- Explain and debug code
- Generate coding practice problems
- Prepare for interviews
- Manage uploaded documents and local conversations
- Switch between multiple local Ollama models without changing the architecture

## Python compatibility verification

The project was validated against Python 3.14.7, which satisfies the requested Python 3.14.x compatibility requirement. The selected packages are compatible with Python 3.14 and were imported successfully in the project environment.

## Architecture

```text
ai-coding-assistant/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── config.py
│   │   ├── database/
│   │   ├── services/
│   │   ├── schemas.py
│   │   └── main.py
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   ├── public/images/
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.cjs
├── data/
│   ├── uploads/
│   ├── chroma_db/
│   └── app.db
├── README.md
├── .gitignore
└── .venv/
```

## Prerequisites

- Python 3.14.x
- Node.js 20+ / npm
- Ollama installed locally
- Git

## Backend setup

1. Open PowerShell in the project root.
2. Create and activate the virtual environment:

```powershell
cd C:\Users\ragha\Desktop\Vscode\RAG-1
.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
cd backend
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

4. Copy the example environment file and adjust values if needed:

```powershell
copy .env.example .env
```

## Frontend setup

```powershell
cd C:\Users\ragha\Desktop\Vscode\RAG-1\frontend
npm install
```

## Ollama installation

Install Ollama and then pull the required local models:

```powershell
ollama pull qwen2.5:3b
ollama pull nomic-embed-text
```

Verify the installed models:

```powershell
ollama list
```

## Start the backend

```powershell
cd C:\Users\ragha\Desktop\Vscode\RAG-1\backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API is available at http://localhost:8000.

## Start the frontend

```powershell
cd C:\Users\ragha\Desktop\Vscode\RAG-1\frontend
npm run dev -- --host 0.0.0.0 --port 5173
```

The app is available at http://localhost:5173.

## Document ingestion

Upload supported files from the Knowledge Base page or via the backend API:

- .txt
- .md
- .pdf
- .docx

The upload pipeline validates the extension and size, extracts text, chunks the content, embeds it with nomic-embed-text, and stores it in ChromaDB.

## Using the RAG chatbot

1. Start Ollama and confirm the models are installed.
2. Start the backend and frontend.
3. Open the app in the browser.
4. Ask a technical question in the chat view.
5. The system retrieves relevant chunks, builds a grounded answer, and shows the source context when available.

## Switching models

The app discovers models from Ollama using the real API rather than hard-coded values. The current default generation model is qwen2.5:3b.

If a different installed model is selected:

- the backend validates it against the model list,
- the request uses that model for generation,
- the embedding model remains separate and is used for vectorization.

## Running tests

From the backend folder:

```powershell
cd backend
..\.venv\Scripts\python.exe -m pytest -q
```

## Troubleshooting

### Ollama is not reachable

Check that Ollama is installed and running:

```powershell
ollama list
```

If needed, start the server:

```powershell
ollama serve
```

### No model found

Pull the missing model:

```powershell
ollama pull qwen2.5:3b
ollama pull nomic-embed-text
```

### Frontend cannot connect to backend

Ensure the backend is running on port 8000 and the frontend is allowed to call that origin.

### ChromaDB is empty

Upload at least one supported document and confirm indexing completes successfully.

## Current limitations

- Local hardware performance affects model speed and vector retrieval latency.
- RAG quality depends on document quality and retrieval settings.
- The app intentionally does not execute uploaded code automatically.
- This is a local application designed for development and demonstration, not a production multi-tenant SaaS platform.

## Future improvements

- Add per-document metadata filtering and richer topic tagging
- Add more robust model-setting persistence in SQLite
- Add real user accounts and authentication
- Add a more advanced debugging workspace and multi-file code analysis
- Add stronger evaluation workflows with explicit rubrics and scoring
