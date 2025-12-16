# Data Model: RAG Chatbot Integration

**Feature Branch**: `003-rag-chatbot-integration`
**Created**: 2025-12-15

## Entities

### Chat Session
Represents a single interaction session between a user and the chatbot.
- `session_id` (UUID): Unique identifier for the session.
- `user_context` (String): Information about the user's current context.
- `current_mode` (Enum: `full-book`, `selected-text`): The current mode of the chatbot.

### User Query
Represents a question submitted by the user.
- `query_id` (UUID): Unique identifier for the query.
- `content` (Text): The actual question text from the user.
- `context_mode` (Enum: `full-book`, `selected-text`): Whether the query is for the full book or selected text.
- `selected_text` (Text, optional): The specific text selected by the user when in selected-text mode.
- `source_metadata` (Object): Metadata about where the query originated (e.g., page, section).

### AI Response
Represents the chatbot's answer to a user query.
- `response_id` (UUID): Unique identifier for the response.
- `content` (Text): The text content of the response.
- `citations` (List of Objects): References to source material. Each object contains:
    - `chapter` (String): The chapter title or identifier.
    - `section` (String): The section title or identifier within the chapter.
- `confidence_level` (Enum: `high`, `medium`, `low`): The system's confidence in the response.

### Document Chunk
Represents a segment of the Docusaurus book content stored in the vector database.
- `chunk_id` (UUID): Unique identifier for the document chunk.
- `content` (Text): The textual content of the chunk.
- `embedding` (Vector): The vector representation of the `content`.
- `source_metadata` (Object): Metadata about the source of the chunk:
    - `chapter` (String): The chapter from which the chunk originated.
    - `section` (String): The section within the chapter.
    - `page_number` (Integer, optional): The page number in the original document.