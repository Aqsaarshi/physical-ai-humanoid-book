# Quickstart: RAG Chatbot Integration

**Feature Branch**: `003-rag-chatbot-integration`
**Created**: 2025-12-15

This guide provides a quick overview to get the RAG Chatbot integrated and running within your Docusaurus book.

## 1. Backend Setup (FastAPI)

### Prerequisites
- Python 3.11+
- `pip` or `pipenv`/`poetry`
- Access to Qdrant Cloud (Free Tier is sufficient)
- Access to Neon Serverless PostgreSQL (Free Tier is sufficient)
- Google Gemini API Key

### Steps

1.  **Clone the repository and navigate to the backend directory:**
    ```bash
    git clone <repository-url>
    cd backend
    ```

2.  **Set up environment variables:**
    Create a `.env` file in the `backend/` directory with the following:
    ```ini
    GEMINI_API_KEY="your_google_gemini_api_key"
    QDRANT_URL="your_qdrant_cloud_url"
    QDRANT_API_KEY="your_qdrant_api_key"
    DATABASE_URL="your_neon_postgresql_connection_string"
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    # Or if using pipenv:
    # pipenv install
    ```

4.  **Run the FastAPI application:**
    ```bash
    uvicorn src.main:app --reload
    ```
    The backend API should now be running, typically at `http://127.0.0.1:8000`. You can access the interactive API documentation at `http://127.0.0.1:8000/docs`.

5.  **Data Ingestion (Initial Indexing)**:
    *   You will need to implement a separate script or endpoint to parse your Docusaurus book content, chunk it, generate embeddings using the Google Gemini API, and upload these vectors to your Qdrant instance. This step is crucial for the RAG functionality.
    *   (Example: `python scripts/ingest_docs.py --book-path ../docs`) - *Note: This script needs to be developed.*

## 2. Frontend Integration (Docusaurus / React)

### Prerequisites
- Node.js (LTS version)
- `npm` or `yarn`
- Existing Docusaurus project

### Steps

1.  **Navigate to your Docusaurus project root:**
    ```bash
    cd frontend # or your docusaurus project root
    ```

2.  **Install frontend dependencies:**
    ```bash
    npm install # or yarn install
    ```

3.  **Integrate the Chatbot React Component:**
    *   Create a new React component for the chatbot UI (e.g., `src/components/Chatbot/index.js`).
    *   This component will handle user input, display responses with citations, manage chat history (via the backend API), and support both full-book and selected-text query modes.
    *   You will need to adapt your Docusaurus theme or layout to include this new chatbot component. This might involve modifying `src/theme/Layout.js` or creating a custom Docusaurus plugin.
    *   Ensure Tailwind CSS is correctly configured for your Docusaurus project if you intend to use it for styling.

4.  **Configure API Endpoints:**
    *   The frontend component will need to know the URL of your backend FastAPI application. This can be configured via Docusaurus' `docusaurus.config.js` or environment variables.

5.  **Run the Docusaurus development server:**
    ```bash
    npm start # or yarn start
    ```
    Your Docusaurus site with the integrated chatbot should now be accessible, typically at `http://localhost:3000`.