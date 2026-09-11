 RAG Chatbot
 Overview

A full-stack RAG chatbot that lets users upload and ask questions about multiple PDF documents. The system retrieves the most relevant parts of the documents, reranks them to improve search quality, and uses an LLM to generate answers with source citations.

The main goal of the project is to build a RAG system that is not limited to a simple vector search. It combines local embeddings, reranking, conversation history, caching, asynchronous processing, and evaluation to make the chatbot more reliable and practical for real-world use.

 Tech Stack

  Backend: FastAPI, Uvicorn
- AI orchestration: LangGraph, LangChain
- Document processing: LlamaIndex, PyMuPDF, pypdf
- Embeddings:Sentence Transformers (BGE / MiniLM)
- Reranking: Cross-Encoder
- Vector Database: Qdrant
- LLM: Groq API
- Caching & sessions: Redis
- Message processing: Kafka
- Database: PostgreSQL
- Evaluation: RAGAS, BERTScore
- Deployment: Docker, Docker Compose
- Frontend: React

How It Works

The chatbot follows a simple retrieval pipeline:


User
  |
  v
React Frontend
  |
  v
FastAPI Backend
  |
  v
LangGraph
  |
  +----> Query Processing
  |
  +----> Vector Search (Qdrant)
  |          |
  |          v
  |     Local Embeddings
  |
  +----> Cross-Encoder Reranking
  |
  v
Relevant Document Chunks
  |
  v
Groq LLM
  |
  v
Answer + Sources
  |
  v
React Frontend


1. Document Upload

Users can upload multiple PDF files. During ingestion, the documents are parsed, split into smaller chunks, converted into embeddings using a local Sentence Transformer model, and stored in Qdrant.

The document metadata and ingestion status are stored separately in PostgreSQL.

2. Retrieval

When the user asks a question, the query is converted into an embedding and searched against the document chunks stored in Qdrant.

Instead of directly sending all retrieved chunks to the LLM, the results are passed through a **Cross-Encoder reranker**. This helps select the chunks that are actually most relevant to the question.

3. Answer Generation

The highest-ranked chunks are added to the LLM prompt as context. The Groq API is then used to generate the final response.

The chatbot also returns the relevant document sources so that the user can see where the answer came from.

4. Conversation History

Chat history is maintained using Redis and PostgreSQL.

Redis is used for fast access to active sessions, while PostgreSQL provides persistent storage for conversations and other application data.

This allows the chatbot to handle follow-up questions such as:

 "What is the main idea of this document?"

followed by:

 "Can you explain the second point in more detail?"

without losing the context of the conversation.

Supporting Services

The application uses a few additional services to make the system easier to scale and maintain:


                 +----------------------+
                 |      FastAPI         |
                 |   Application API    |
                 +----------+-----------+
                            |
                         LangGraph
                            |
          +-----------------+----------------+
          |                 |                |
          v                 v                v
       Qdrant            Redis           Groq API
     Vector Search    Cache / Session       LLM
          |
          v
   Local Embeddings
    Cross-Encoder


          FastAPI
             |
      +------+-------+-------------+
      |              |             |
      v              v             v
   Kafka         PostgreSQL     Evaluation
   Events        Persistence      RAGAS
                                BERTScore


Redis

Used for:

- Active chat sessions
- Conversation history
- Frequently repeated queries
- Temporary application state

Kafka

Kafka is used for background and event-based processing.

For example, PDF ingestion can be handled asynchronously instead of making the user wait for the entire indexing process. Chat interactions can also be published as events for logging and analytics.

PostgreSQL

Stores persistent application data such as:

- Uploaded document metadata
- Ingestion status
- Chat conversations
- User/session information
- Evaluation results

Why Local Embeddings and Reranking?

One of the main design decisions in this project is keeping the retrieval models local.

Instead of sending every document chunk to an external embedding API, Sentence Transformer models are run locally using PyTorch.

A Cross-Encoder is then used to rerank the retrieved chunks.

This gives more control over the retrieval pipeline and avoids additional API costs for the retrieval stage.

The LLM is only used for the generation step through the Groq API.

## Evaluation

The system is evaluated using a small test dataset containing questions, expected answers, and relevant document context.

RAGAS is used to evaluate aspects such as:

- Faithfulness
- Answer relevancy
- Context relevancy
- Retrieval quality

BERTScore is also used to compare generated answers with reference answers.

This makes it possible to experiment with different embedding models, chunk sizes, retrieval limits, and reranking strategies instead of relying only on subjective testing.

 Docker Setup

The application is containerized using Docker and Docker Compose.

The development environment can run the main services together:
React
FastAPI
Qdrant
Redis
Kafka
PostgreSQL


This makes the project easier to set up and provides a setup that is closer to how a production RAG application could be deployed.

Key Features

- Multi-PDF document upload
- Local PyTorch-based embeddings
- Semantic search with Qdrant
- Cross-Encoder reranking
- LangGraph-based RAG workflow
- Groq-powered answer generation
- Source citations in responses
- Conversation memory
- Redis caching
- Asynchronous document ingestion
- Kafka event processing
- PostgreSQL persistence
- RAGAS and BERTScore evaluation
- Dockerized development environment
- Streaming responses

Project Goal

This project was built to understand what goes beyond a basic "PDF + vector database + LLM" chatbot.

The focus is on building the individual parts of a RAG system—**document ingestion, retrieval, reranking, generation, memory, caching, asynchronous processing, and evaluation**—and connecting them into one complete application.