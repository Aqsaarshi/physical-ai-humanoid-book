# Tasks for RAG Chatbot Integration

**Feature Name**: RAG Chatbot Integration  
**Branch**: `002-rag-chatbot-integration`  
**Date**: 2025-12-06  
**Spec**: `E:\Hackathon book\book\specs\002-rag-chatbot-integration\spec.md`  
**Plan**: `E:\Hackathon book\book\specs\002-rag-chatbot-integration\plan.md`

---

## Implementation Strategy

This feature will be implemented incrementally, prioritizing core functionality first. Each User Story will be developed as a distinct phase, allowing for independent testing and validation.

---

## Phase 1: Setup

**Goal**: Initialize project structure and install core dependencies.

- [x] T001 Setup backend directories  
  `backend/src/models/`, `backend/src/services/`, `backend/src/api/`, `backend/tests/`
- [x] T002 Setup frontend directories  
  `frontend/src/components/`, `frontend/src/pages/`, `frontend/src/services/`, `frontend/tests/`
- [x] T003 Install Python dependencies for backend in `backend/requirements.txt`
- [x] T004 Install Node.js dependencies for frontend in `frontend/package.json`
- [x] T005 Configure environment variables for Qdrant and Neon DB connections in `.env`

---

## Phase 2: Foundational Components

**Goal**: Establish connections to external services and implement document ingestion.

- [x] T006 Connect to Qdrant vector database in `backend/src/services/qdrant_service.py`
- [x] T007 Connect to Neon Serverless PostgreSQL database in `backend/src/services/db_service.py`
- [x] T008 Implement document chunking and ingestion process for Docusaurus book content in  
  `backend/src/services/ingestion_service.py`
- [x] T009 Implement text embedding generation using cohere in  
  `backend/src/services/cohere_service.py`
- [x] T010 Implement vector search and retrieval (RAG) query logic in  
  `backend/src/services/rag_service.py`

---

## Phase 3: User Story 1 (P1) – Ask about Entire Book

**Goal**: User can ask questions about the entire Docusaurus book content and receive accurate answers.  
**Independent Test**: Ask a question covering broad topics within the book and verify the response’s accuracy and relevance.

- [x] T011 [US1] Create Chat Conversation model in `backend/src/models/chat.py`
- [x] T012 [US1] Create Chat Message model in `backend/src/models/chat.py`
- [x] T013 [US1] Create endpoint `/chat/ask` in `backend/src/api/chat.py`
- [x] T014 [US1] Integrate RAG service into `/chat/ask` endpoint
- [x] T015 [US1] Implement citation generation in `backend/src/services/citation_service.py`
- [x] T016 [US1] Build ChatWidget UI component in  
  `frontend/src/components/ChatWidget.tsx`
- [x] T017 [US1] Integrate ChatWidget into Docusaurus page  
  `frontend/src/pages/chatbot.tsx`

---

## Phase 4: User Story 2 (P1) – Ask Based on Selected Text

**Goal**: User can select specific text and ask questions based only on that text.  
**Independent Test**: Select a paragraph, ask a question relevant only to that paragraph, and verify the answer strictly uses the selected text.

- [x] T018 [P][US2] Modify `/chat/ask` endpoint to accept `selected_text`
- [x] T019 [P][US2] Update RAG service to prioritize selected text context
- [x] T020 [US2] Implement text selection mechanism in  
  `frontend/src/services/text_selection.ts`
- [x] T021 [US2] Integrate text selection with ChatWidget

---

## Phase 5: User Story 3 (P2) – Streamed Responses

**Goal**: Chatbot responses are streamed in real-time.  
**Independent Test**: Verify text appears progressively.

- [x] T022 [US3] Modify `/chat/ask` endpoint to stream responses (SSE/WebSockets)
- [x] T023 [US3] Update ChatWidget to handle streamed responses

---

## Phase 6: User Story 4 (P2) – Chat History Persistence

**Goal**: Chat history is saved and retrievable across sessions.  
**Independent Test**: Reload site and verify previous messages load.

- [x] T024 [US4] Implement CRUD operations for chat history
- [x] T025 [US4] Integrate chat history saving into `/chat/ask`
- [x] T026 [US4] Create endpoint to retrieve chat history
- [x] T027 [US4] Build ChatHistory UI component
- [x] T028 [US4] Integrate ChatHistory into chatbot page

---

## Phase 7: User Story 5 (P3) – Clear Error Messages

**Goal**: Provide clear and helpful error messages.  
**Independent Test**: Ask out-of-scope questions and simulate errors.

- [x] T029 [US5] Custom exception handling in `rag_service.py`
- [x] T030 [US5] Global exception handling in `backend/src/main.py`
- [x] T031 [US5] Display user-friendly errors in ChatWidget

---

## Phase 8: Polish & Cross-Cutting Concerns

**Goal**: Ensure quality, testing, and deployment readiness.

- [x] T032 Unit tests for backend services
- [x] T033 Integration tests for backend APIs
- [ ] T034 Frontend component tests for ChatWidget
- [ ] T035 Document APIs using cohere (Swagger UI)
- [ ] T036 Update Docusaurus navigation to include chatbot page
- [ ] T037 Prepare deployment scripts (Docker/cloud)

---

## Dependencies

- Phase 1 must complete before any other phase  
- Phase 2 must complete before User Story phases  
- User Stories (3–7) have minimal inter-dependencies, prioritize P1

---

## Parallel Execution Examples

- **User Story 1**: T011 & T012 → parallel; T013 & T014 → parallel; T016 & T017 → parallel  
- **User Story 2**: T018 & T019 → parallel; T020 & T021 → parallel  
- **User Story 3**: T022 & T023 → parallel  
- **User Story 4**: T024, T025, T026 → parallel; T027 & T028 → parallel  
- **User Story 5**: T029, T030, T031 → parallel

---

## Suggested MVP Scope

For MVP, focus on:
- **Phase 1 (Setup)**
- **Phase 2 (Foundational Components)**
- **Phase 3 (User Story 1 – Ask about Entire Book)**

This delivers a fully functional and independently testable RAG chatbot.
