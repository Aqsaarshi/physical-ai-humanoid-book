import os
import re
import sys
from typing import List

# from .qdrant_service import get_qdrant_client
# from .openai_service import get_embedding


def load_docusaurus_content(docs_path: str = "../../docs") -> List[str]:
    """
    Load all markdown (.md/.mdx) files from the Docusaurus docs folder.
    """
    content = []
    for root, _, files in os.walk(docs_path):
        for file in files:
            if file.endswith(".md") or file.endswith(".mdx"):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content.append(f.read())
    return content


def chunk_text(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> List[str]:
    """
    Chunk text into smaller pieces for RAG ingestion.
    Splits by paragraphs and further splits if section is too large.
    """
    chunks = []
    current_chunk = ""

    # Split by major sections or paragraphs
    sections = re.split(r'\n\n+', text)

    for section in sections:
        if len(current_chunk) + len(section) < chunk_size:
            current_chunk += "\n\n" + section
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = section

        # If a single section is too large, split it further
        while len(current_chunk) > chunk_size:
            split_point = current_chunk.rfind(' ', 0, chunk_size)
            if split_point == -1:
                split_point = chunk_size  # Fallback to hard split
            chunks.append(current_chunk[:split_point].strip())
            current_chunk = current_chunk[split_point - chunk_overlap:].strip()

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def ingest_documents(docs_path: str = "../../docs", collection_name: str = "docusaurus_docs"):
    """
    Ingest documents into vector DB (Qdrant) with Google AI embeddings.
    """
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    from src.services.qdrant_service import QdrantService
    from src.services.retrieval_service import RetrievalService

    try:
        qdrant_service = QdrantService()
        documents = load_docusaurus_content(docs_path)

        print(f"Found {len(documents)} documents to ingest")

        for doc_idx, doc in enumerate(documents):
            chunks = chunk_text(doc)
            print(f"Processing document {doc_idx + 1}/{len(documents)} with {len(chunks)} chunks")

            for chunk_idx, chunk in enumerate(chunks):
                doc_id = f"{doc_idx}_{chunk_idx}"
                metadata = {"source": f"doc_{doc_idx}", "chunk": chunk_idx}

                try:
                    success = qdrant_service.upsert_document(
                        doc_id=doc_id,
                        content=chunk,
                        metadata=metadata
                    )
                    if success:
                        print(f"  Successfully ingested chunk {chunk_idx + 1}")
                    else:
                        print(f"  Failed to ingest chunk {chunk_idx + 1}")
                except Exception as e:
                    print(f"  Error ingesting chunk {chunk_idx + 1}: {str(e)}")

        print("Document ingestion completed successfully.")
        return True
    except Exception as e:
        print(f"Error during document ingestion: {str(e)}")
        return False


if __name__ == "__main__":
    # Example usage (will be replaced by FastAPI endpoint trigger)
    print("Starting document ingestion...")
    success = ingest_documents()
    if success:
        print("Ingestion completed successfully!")
    else:
        print("Ingestion failed!")
