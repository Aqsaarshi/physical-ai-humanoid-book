import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from services.ingestion_service import ingest_documents

if __name__ == "__main__":
    print("Starting document ingestion...")
    success = ingest_documents(docs_path='../docs', collection_name='book_content')
    if success:
        print("Ingestion completed successfully!")
    else:
        print("Ingestion failed!")