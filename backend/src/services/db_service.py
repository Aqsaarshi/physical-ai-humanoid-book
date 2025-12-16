import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# Create the declarative base
Base = declarative_base()


class DatabaseService:
    def __init__(self):
        self.engine = create_engine(
            settings.database_url,
            pool_pre_ping=True,
            pool_recycle=300,
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_db(self):
        """
        Dependency to get database session
        """
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def get_engine(self):
        """
        Get the database engine
        """
        return self.engine


# Create a global instance
db_service = DatabaseService()
