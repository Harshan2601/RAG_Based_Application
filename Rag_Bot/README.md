# RAG-Powered Document Chat Assistant

A full-stack Retrieval-Augmented Generation (RAG) application that lets users upload their own documents and ask questions about them through a chat interface. Instead of answering purely from what the model already knows, the system looks up relevant passages from the uploaded documents first and then generates an answer grounded in that context, along with citations back to the source.

Status: work in progress.

## Why this project

Most LLM chatbots answer from whatever they learned during training, which means they can confidently make things up when asked about private or domain-specific material they were never trained on. This project gets around that by pairing an LLM with a retrieval step: documents are chunked, embedded, and stored in a vector database, and at query time the most relevant chunks are pulled in as context before the model generates a response.

Broadly, the goals for this project are:

- Let users upload and process multiple documents
- Search across that content semantically, not just by keyword
- Retrieve relevant context before generating an answer
- Return answers with citations back to the source material
- Keep conversational context across a session
- Use Redis for caching and session state
- Wrap it all in a full-stack web app that's easy to run with Docker

## Architecture

```
React Frontend
  - Chat interface
  - Document upload
  - Source citations
        |
        | REST API
        v
FastAPI Backend
  - Authentication
  - Document processing
  - Chat orchestration
  - RAG pipeline
        |
        |-----------------------|
        v                       v
     Redis                Vector Store
  - Sessions             - Embeddings
  - Cache                - Semantic retrieval
  - Context                    |
                                v
                           Retriever
                          - Top-K chunks
                                |
                                v
                              LLM
                          - Generation
                                |
                                v
                     Answer + sources
```

## Tech stack

The frontend is built in React and handles the chat UI, document uploads, and displaying source citations alongside answers. The backend is Python with FastAPI, handling document processing, chat orchestration, and the RAG pipeline itself. Document chunks and queries are converted into vectors with an embedding model and stored in a vector database (Qdrant or ChromaDB, still being finalized). Redis handles sessions, caching, and conversational state, and the whole thing is containerized with Docker so it runs the same way locally and in production. Frontend and backend talk over a REST API, and the code is versioned with Git on GitHub.

## How it works

The application follows a fairly standard ingestion-then-query pipeline for RAG systems.

**Uploading a document.** A user uploads one or more files through the React interface. That request goes to the FastAPI backend, which kicks off processing.

**Processing.** The backend extracts text from the document, cleans it up, and splits it into smaller chunks. Chunking matters here — it means the system only has to retrieve the sections that are actually relevant to a question, instead of stuffing the entire document into the model's context window every time.

**Embedding and storage.** Each chunk gets converted into a vector representation by an embedding model, and those vectors are stored in the vector database for later retrieval.

**Asking a question.** The user sends a question through the chat interface, which goes to FastAPI the same way an upload does.

**Retrieval.** The question itself gets embedded, and that embedding is compared against the stored document vectors to find the most similar chunks — the ones most likely to actually answer the question.

**Generation.** Those retrieved chunks, along with the original question, get passed to the LLM, which generates an answer grounded in that context rather than just its own general knowledge.

**Returning the answer.** The backend sends back the generated answer together with references to the source chunks it used, so the response shows up in the chat interface with citations attached. That's what gives users a way to actually verify where an answer came from, rather than just trusting it blindly.

## Redis

Redis sits between FastAPI and everything else as a fast in-memory layer. It's used for session management, keeping track of conversation state, caching frequently asked queries, and general temporary data the app needs quick access to. Nothing here depends on a slow database round-trip.

## Docker setup

Everything runs as containers — the React app, the FastAPI API, Redis, and the vector database. The frontend and backend talk over REST, and Docker Compose ties it all together so the same setup works in development and in production without surprises.

## Where this could be used

A few scenarios this kind of system fits well:

**Enterprise knowledge assistant** — employees querying internal policies, technical docs, process manuals, and SOPs without digging through folders.

**Customer support** — support teams pointing the assistant at product manuals, FAQs, and troubleshooting guides so it can answer with cited sources instead of guessing.

**Legal and compliance** — working through contracts, regulations, and compliance documents where being able to trace an answer back to the original text actually matters.

**Academic research** — students and researchers uploading papers, lecture notes, or books and asking questions directly against that material.

**Employee onboarding** — new hires getting answers from handbooks, training materials, and internal documentation instead of waiting on someone else.

**Personal use** — just uploading your own notes, reports, or study material and querying them like a personal knowledge base.

## Features

- Multi-document upload
- Semantic search across document content
- LLM-generated answers grounded in retrieved context
- Source citations attached to responses
- Conversational, session-aware chat
- Redis-backed caching and session state
- Fully containerized with Docker
- REST API between frontend and backend
- Modular backend designed to scale

## Project structure

```
rag-document-chat/
|
|-- frontend/
|   |-- src/
|   |-- public/
|   |-- package.json
|   |-- Dockerfile
|
|-- backend/
|   |-- auth/
|   |-- chat/
|   |-- documents/
|   |-- rag/
|   |-- retriever/
|   |-- services/
|   |-- main.py
|   |-- requirements.txt
|   |-- Dockerfile
|
|-- data/
|
|-- docker-compose.yml
|-- .env.example
|-- .gitignore
|-- README.md
```

## Getting started

You'll need Node.js 18+, Python 3.10+, Docker and Docker Compose, Git, a running Redis instance, a vector database, and an API key for whichever LLM you're using.

Clone the repo:

```bash
git clone https://github.com/<your-username>/<repository-name>.git
cd <repository-name>
```

### Backend

```bash
cd backend
python -m venv venv
```

Activate the virtual environment — on Windows:

```bash
venv\Scripts\activate
```

on Linux/macOS:

```bash
source venv/bin/activate
```

Then install dependencies and start the server:

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

In a separate terminal:

```bash
cd frontend
npm install
npm start
```

## Environment variables

Copy `.env.example` to `.env` and fill in the values:

```env
LLM_API_KEY=your_api_key
REDIS_URL=redis://localhost:6379
VECTOR_DB_URL=your_vector_database_url
```

Don't commit real API keys or credentials to the repo — keep them in `.env` and make sure it's gitignored.

## Running with Docker

Build and start everything:

```bash
docker compose up --build
```

Shut it down:

```bash
docker compose down
```

## API flow

**Uploading a document:** `POST /documents/upload` triggers document processing, then text chunking, then embedding generation, and the resulting vectors land in the vector database.

**Asking a question:** `POST /chat` processes the query, embeds it, runs semantic retrieval to pull relevant chunks, builds context from them, sends that to the LLM for generation, and returns the answer along with its sources.

## What's next

This is still an early-stage project, and there's a fair amount left to build:

- User authentication and authorization
- Multi-user document management
- Streaming responses instead of waiting for the full answer
- Better long-term conversation memory
- A proper document management dashboard
- Tighter citation and source tracking
- Role-based access control
- Actual evaluation and benchmarking of retrieval quality
- Automated tests and a CI/CD pipeline
- Monitoring and logging once this moves toward production
- Support for more document formats
- Better retrieval — reranking, hybrid keyword + semantic search

## Why I'm building this

This project is mostly a way to get hands-on with generative AI and RAG in particular — working through vector search, semantic retrieval, and how to wire an LLM up to a real knowledge base, while also building out the full-stack and infrastructure side: FastAPI, REST API design, Redis, Docker, and generally what it takes to move something like this toward production.

## Portfolio

https://harshanramesh.netlify.app/
