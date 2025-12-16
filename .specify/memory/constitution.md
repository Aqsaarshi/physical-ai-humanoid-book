<!--
Sync Impact Report:
Version change: 1.2.0 -> 1.3.0
Modified principles: Refined principles for RAG Chatbot development.
Added sections: Project Overview.
Removed sections: None.
Templates requiring updates:
- .specify/templates/plan-template.md: ⚠ pending (review for RAG chatbot planning alignment)
- .specify/templates/spec-template.md: ⚠ pending (review for RAG chatbot specification alignment)
- .specify/templates/tasks-template.md: ⚠ pending (review for RAG chatbot task generation alignment)
- .specify/templates/commands/*.md: ⚠ pending (review for any command-specific guidance related to RAG chatbot)
- README.md: ⚠ pending (update with new project scope/constitution link)
- docs/quickstart.md: ⚠ pending (update with chatbot quickstart relevant to new stack)
Follow-up TODOs: Review and update any other project-specific documentation or configuration.
-->
# Docusaurus RAG Chatbot Project Constitution

## Project Overview

**Goal**: Integrate a fully functional RAG chatbot within your Docusaurus book, which can answer any user question based on the book content, including selected text, and provide citations.

**Core Features**:
- Ask about entire book content.
- Ask based on user-selected text.
- Streamed responses (dynamic UI).
- Chat history persistence.
- Citation for every answer.
- Error handling and user-friendly messages.

## Core Principles

### 1. Clean Architecture
MUST adhere to a clean architecture (e.g., layered architecture) to ensure separation of concerns, testability, and maintainability. Components MUST be loosely coupled and highly cohesive, especially within the RAG chatbot's modular design.

### 2. Document-Based Retrieval (No Hallucination & Citation)
MUST ONLY generate responses based on content retrieved from the designated document store (RAG). The system MUST actively prevent hallucination by strictly limiting the LLM's response generation to the provided context. Every answer MUST provide clear citations to the source material within the Docusaurus book.

### 3. Safety and Scope Adherence
MUST NOT answer questions outside the scope of the Docusaurus book content UNLESS the user explicitly provides relevant selected text. Mechanisms MUST be in place to detect and respond appropriately to out-of-scope queries.

### 4. Context-First Reasoning
MUST prioritize retrieved context over general LLM knowledge when formulating responses. The LLM's reasoning MUST primarily synthesize and summarize information present in the provided document chunks, ensuring relevance to the book content.

### 5. Clear Error Explanation
MUST provide clear, concise, and actionable error messages to the user within the chatbot UI. Internal errors MUST be logged comprehensively for debugging without exposing sensitive details to the end-user.

### 6. End-to-End Reproducibility
The entire RAG pipeline, from document ingestion to response generation, MUST be reproducible. This includes versioning of data, code, and model configurations to ensure consistent behavior across environments.

## Technology Stack

- **OpenAI Agents / ChatKit SDKs**: For LLM interaction, agent orchestration, and conversation management.
- **FastAPI backend**: For building robust and scalable API endpoints to serve the chatbot.
- **Neon Serverless PostgreSQL database**: For persistent storage of chat history, user interactions, and potentially other application data.
- **Qdrant Cloud Free Tier (vector DB)**: Primary vector database for storing and retrieving document embeddings from the Docusaurus book content.
- **Docusaurus frontend**: The main platform where the chatbot will be integrated.
- **Tailwind CSS / React for chatbot UI**: For building a modern, responsive, and user-friendly chatbot interface.

## Governance

This section outlines the process for maintaining and evolving this constitution.

### Amendment Procedure
Amendments to this constitution MUST be proposed via a Pull Request (PR) and require review and approval from at least two core project maintainers.

### Versioning Policy
This constitution adheres to Semantic Versioning (MAJOR.MINOR.PATCH):
- **MAJOR**: Backward incompatible changes, principle removals, or fundamental redefinitions.
- **MINOR**: Additions of new principles, new sections, or material expansions of existing guidance.
- **PATCH**: Clarifications, wording improvements, typo fixes, or non-semantic refinements.

### Compliance Review
The project's adherence to these principles MUST be reviewed quarterly or after any major architectural change.

**Version**: 1.3.0 | **Ratified**: 2025-12-03 | **Last Amended**: 2025-12-06