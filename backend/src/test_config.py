import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import settings

print("Settings loaded successfully!")
print(f"Gemini API Key: {settings.gemini_api_key[:10]}...")
print(f"Qdrant URL: {settings.qdrant_url}")
print(f"Database URL: {settings.database_url}")