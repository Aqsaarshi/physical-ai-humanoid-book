# Data Model: RAG Chatbot Integration

**Feature Branch**: `002-rag-chatbot-integration`
**Created**: 2025-12-06

## Entities

### Chat Conversation
Represents a continuous dialogue between a user and the chatbot.
- `conversation_id` (UUID): Unique identifier for the conversation.
- `user_id` (String): Identifier for the user associated with the conversation.
- `start_time` (Timestamp): The time when the conversation was initiated.
- `last_active_time` (Timestamp): The last time a message was sent or received in the conversation.

### Chat Message
Represents a single message within a conversation, either from the user or the chatbot.
- `message_id` (UUID): Unique identifier for the message.
- `conversation_id` (UUID): Foreign key linking to the `Chat Conversation`.
- `sender` (Enum: `user`, `bot`): Indicates who sent the message.
- `content` (Text): The actual text content of the message.
- `timestamp` (Timestamp): The time when the message was sent.
- `citations` (List of Objects): References to source material. Each object contains:
    - `chapter` (String): The chapter title or identifier.
    - `section` (String): The section title or identifier within the chapter.

### Document Chunk
Represents a segment of the Docusaurus book content stored in the vector database.
- `chunk_id` (UUID): Unique identifier for the document chunk.
- `content` (Text): The textual content of the chunk.
- `embedding` (Vector): The vector representation of the `content`.
- `source_metadata` (Object): Metadata about the source of the chunk:
    - `chapter` (String): The chapter from which the chunk originated.
    - `section` (String): The section within the chapter.
    - `page_number` (Integer, optional): The page number in the original document.

### User Selection
Represents the specific text selected by the user for context-restricted questions.
- `selected_text` (Text): The actual text selected by the user.
- `source_metadata` (Object): Metadata about the source of the selection:
    - `chapter` (String): The chapter from which the text was selected.
    - `section` (String): The section within the chapter.
