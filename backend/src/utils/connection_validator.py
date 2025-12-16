import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.qdrant_service import QdrantService
from services.db_service import db_service
from config import settings
import psycopg2
from google.generativeai import configure
import logging

logger = logging.getLogger(__name__)


class ConnectionValidator:
    @staticmethod
    def validate_gemini_connection():
        """
        Validate Google Gemini API connection
        """
        try:
            configure(api_key=settings.gemini_api_key)
            # Test basic configuration by attempting to list models
            import google.generativeai as genai
            models = genai.list_models()
            return True
        except Exception as e:
            logger.error(f"Error validating Gemini connection: {str(e)}")
            return False

    @staticmethod
    def validate_qdrant_connection():
        """
        Validate Qdrant Cloud connection
        """
        try:
            qdrant_service = QdrantService()
            # Test by getting collections
            collections = qdrant_service.client.get_collections()
            return True
        except Exception as e:
            logger.error(f"Error validating Qdrant connection: {str(e)}")
            return False

    @staticmethod
    def validate_database_connection():
        """
        Validate Neon PostgreSQL connection
        """
        try:
            # Try to connect to the database
            db_gen = db_service.get_db()
            db = next(db_gen)
            # Execute a simple query
            db.execute("SELECT 1")
            return True
        except Exception as e:
            logger.error(f"Error validating database connection: {str(e)}")
            return False

    @staticmethod
    def validate_all_connections():
        """
        Validate all external service connections
        """
        gemini_ok = ConnectionValidator.validate_gemini_connection()
        qdrant_ok = ConnectionValidator.validate_qdrant_connection()
        db_ok = ConnectionValidator.validate_database_connection()

        return {
            "gemini": gemini_ok,
            "qdrant": qdrant_ok,
            "database": db_ok,
            "all_valid": gemini_ok and qdrant_ok and db_ok
        }