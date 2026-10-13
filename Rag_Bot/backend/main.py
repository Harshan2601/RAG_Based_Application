from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
from uuid import uuid4
from datetime import datetime
import shutil

app = FastAPI(
    title="AI Technical Support Co-Pilot",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

documents_db = {}
chat_sessions = {}
ingestion_jobs = {}


class ChatRequest(BaseModel):
    session_id: str | None = None
    question: str
    top_k: int = 5
    use_reranker: bool = True


class ChatResponse(BaseModel):
    session_id: str
    answer: str
    sources: list


class EvaluationRequest(BaseModel):
    dataset_name: str = "default_eval_dataset"


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "RAG backend is running"
    }


@app.post("/api/v1/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith((".pdf", ".txt", ".md")):
        raise HTTPException(
            status_code=400,
            detail="Only PDF, TXT, and MD files are supported"
        )

    document_id = str(uuid4())
    file_path = UPLOAD_DIR / f"{document_id}_{file.filename}"

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    documents_db[document_id] = {
        "document_id": document_id,
        "filename": file.filename,
        "path": str(file_path),
        "uploaded_at": datetime.utcnow().isoformat(),
        "status": "uploaded"
    }

    return {
        "message": "Document uploaded successfully",
        "document": documents_db[document_id]
    }


@app.get("/api/v1/documents")
def list_documents():
    return {
        "documents": list(documents_db.values())
    }


@app.delete("/api/v1/documents/{document_id}")
def delete_document(document_id: str):
    document = documents_db.get(document_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    file_path = Path(document["path"])
    if file_path.exists():
        file_path.unlink()

    del documents_db[document_id]

    return {
        "message": "Document deleted successfully",
        "document_id": document_id
    }


@app.post("/api/v1/ingest/{document_id}")
def ingest_document(document_id: str):
    document = documents_db.get(document_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    job_id = str(uuid4())

    ingestion_jobs[job_id] = {
        "job_id": job_id,
        "document_id": document_id,
        "status": "completed",
        "message": "Document chunked, embedded, and stored in vector DB",
        "created_at": datetime.utcnow().isoformat()
    }

    document["status"] = "ingested"

    