# Tasks for RAG Chatbot Integration

**Feature Name**: Embedded RAG Chatbot in Docusaurus Book
**Branch**: `003-rag-chatbot-integration`
**Date**: 2025-12-15
**Spec**: `E:\Hackathon book\book\specs\003-rag-chatbot-integration\spec.md`
**Plan**: `E:\Hackathon book\book\specs\003-rag-chatbot-integration\plan.md`

---
## Implementation Strategy

This feature will be implemented incrementally, prioritizing core functionality first. Each User Story will be developed as a distinct phase, allowing for independent testing and validation.

---

## Phase 1: Backend Environment & Configuration

**Goal**: Set up the backend environment and validate all external service connections.

- [x] T001 Setup backend project structure in `backend/`
- [x] T002 [P] Create requirements.txt with FastAPI, Google AI SDK, Qdrant Client, psycopg2 dependencies
- [x] T003 [P] Create .env file template with GEMINI_API_KEY, QDRANT_URL, QDRANT_API_KEY, DATABASE_URL
- [x] T004 [P] Configure environment variable loading in `backend/src/config.py`
- [x] T005 Configure Google AI SDK client to use Gemini models in `backend/src/services/gemini_service.py`
- [x] T006 Configure Qdrant Cloud connection in `backend/src/services/qdrant_service.py`
- [x] T007 Configure Neon PostgreSQL connection in `backend/src/services/db_service.py`
- [x] T008 Create connection validation utilities in `backend/src/utils/connection_validator.py`

---

## Phase 2: Data Models & Persistence

**Goal**: Implement data models and persistence layer for chat history.

- [x] T009 Create SQLAlchemy models for ChatSession in `backend/src/models/chat_session.py`
- [x] T010 Create SQLAlchemy models for UserQuery in `backend/src/models/user_query.py`
- [x] T011 Create SQLAlchemy models for AIResponse in `backend/src/models/ai_response.py`
- [x] T012 [P] Create database migrations for all models in `backend/src/db/migrations/`
- [x] T013 Create repository layer for ChatSession in `backend/src/repositories/chat_session_repo.py`
- [x] T014 [P] Create repository layer for UserQuery in `backend/src/repositories/user_query_repo.py`
- [x] T015 [P] Create repository layer for AIResponse in `backend/src/repositories/ai_response_repo.py`

---

## Phase 3: RAG Retrieval Core

**Goal**: Implement the core RAG retrieval functionality for the "002-physical-ai-robotics-textbook".

- [x] T016 Validate Qdrant collections for "002-physical-ai-robotics-textbook" in `backend/src/services/qdrant_service.py`
- [x] T017 Implement semantic retrieval logic in `backend/src/services/retrieval_service.py`
- [x] T018 [P] Implement context filtering and ranking in `backend/src/services/retrieval_service.py`
- [x] T019 [P] Implement strict grounding enforcement to ensure book-only answers in `backend/src/services/validation_service.py`
- [x] T020 [P] Create citation-ready context packaging in `backend/src/services/citation_service.py`

---

## Phase 4: Gemini Answer Generation

**Goal**: Implement answer generation using Google Gemini with RAG context.

- [x] T021 Create RAG prompt construction utility in `backend/src/services/prompt_service.py`
- [x] T022 [P] Implement Gemini invocation via Google AI SDK in `backend/src/services/gemini_service.py`
- [x] T023 [P] Add response validation against retrieved context in `backend/src/services/validation_service.py`
- [x] T024 [P] Implement latency and token safeguards in `backend/src/services/gemini_service.py`

---

## Phase 5: Selected-Text Question Answering

**Goal**: Implement the ability to answer questions based only on selected text.

- [x] T025 [P] [US2] Update API to support selected-text input in `backend/src/api/chat.py`
- [x] T026 [P] [US2] Implement context isolation for selected text only in `backend/src/services/retrieval_service.py`
- [x] T027 [US2] Explicitly disable full-book retrieval when in selected-text mode in `backend/src/services/retrieval_service.py`

---

## Phase 6: FastAPI Endpoints

**Goal**: Create FastAPI endpoints that comply with the OpenAPI contract.

- [x] T028 [P] [US1] Create POST /chat/book endpoint in `backend/src/api/chat.py`
- [x] T029 [P] [US2] Create POST /chat/selected-text endpoint in `backend/src/api/chat.py`
- [x] T030 [P] [US1] [US2] Add request validation for both endpoints in `backend/src/schemas/chat.py`
- [x] T031 [P] [US1] [US2] Add error handling for both endpoints in `backend/src/api/chat.py`
- [x] T032 [P] [US1] [US2] Ensure OpenAPI contract compliance with spec in `backend/src/api/chat.py`

---

## Phase 7: Docusaurus Integration

**Goal**: Embed the chatbot UI in the "002-physical-ai-robotics-textbook" book.

- [x] T033 [P] [US3] Create React chatbot component in `frontend/src/components/Chatbot/Chatbot.tsx`
- [x] T034 [P] [US3] Implement API integration with FastAPI backend in `frontend/src/services/chatbot_api.ts`
- [x] T035 [P] [US2] [US3] Implement selected-text capture from Docusaurus content in `frontend/src/components/Chatbot/TextSelection.tsx`
- [x] T036 [US3] Add minimal loading and error states in `frontend/src/components/Chatbot/Chatbot.tsx`
- [x] T037 [US3] Integrate chatbot component into "002-physical-ai-robotics-textbook" layout in `frontend/src/theme/ChatbotContainer.tsx`

---

## Phase 8: Validation & Reproducibility

**Goal**: Validate implementation against specification and ensure reproducibility.

- [x] T038 [P] Write unit tests for retrieval logic in `backend/tests/unit/test_retrieval_service.py`
- [x] T039 [P] Write API integration tests in `backend/tests/integration/test_chat_api.py`
- [x] T040 [P] Verify end-to-end reproducibility in `backend/src/utils/reproducibility_check.py`
- [x] T041 [P] Perform final validation against spec acceptance criteria in `tests/acceptance/`

---

## Dependencies

- Phase 1 must complete before any other phase
- Phase 2 must complete before RAG retrieval and API endpoints
- Phase 3 must complete before Gemini answer generation
- Phase 4 must complete before API endpoints (Phase 6)
- Phase 6 must complete before Docusaurus integration (Phase 7)

---

## Parallel Execution Examples

- **Phase 1**: T002, T003, T004 → parallel; T005, T006, T007 → parallel
- **Phase 2**: T009, T010, T011 → parallel; T013, T014, T015 → parallel
- **Phase 3**: T017, T018, T019 → parallel; T020 → sequential after others
- **Phase 4**: T021, T022, T023, T024 → parallel
- **Phase 5**: T025, T026 → parallel; T027 → after T026
- **Phase 6**: T028, T029 → parallel; T030, T031, T032 → parallel
- **Phase 7**: T033, T034, T035 → parallel; T036 → after T033; T037 → after all others
- **Phase 8**: T038, T039, T040, T041 → parallel

---

## Suggested MVP Scope

For MVP, focus on:
- **Phase 1** (Backend Environment & Configuration)
- **Phase 2** (Data Models & Persistence)
- **Phase 3** (RAG Retrieval Core)
- **Phase 4** (Gemini Answer Generation)
- **Phase 6** (FastAPI Endpoints) - specifically T028 for full-book Q&A
- **Phase 7** (Docusaurus Integration) - specifically T033, T034, T036, T037

This delivers a fully functional RAG chatbot that allows users to ask questions about the entire book with citations, embedded in the Docusaurus book.