import os
import sys
from sqlmodel import SQLModel, create_engine
from sqlalchemy import text

# Add the backend/src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.config import settings
from src.models.user import User
from src.models.task import Task

def reset_database():
    """Reset the database by dropping and recreating all tables."""
    print("Connecting to database...")

    # Create engine with the database URL from settings
    engine = create_engine(settings.database_url)

    print("Dropping all tables...")
    # Drop all existing tables
    SQLModel.metadata.drop_all(engine)
    print("All tables dropped.")

    print("Creating new tables with updated schema...")
    # Create tables with the updated schema
    SQLModel.metadata.create_all(engine)
    print("Database reset complete!")

    # Verify the user table has the hashed_password column
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = 'user' AND column_name = 'hashed_password'
        """))
        columns = result.fetchall()

        if columns:
            print(f"✓ Verified: hashed_password column exists in user table: {columns}")
        else:
            print("✗ ERROR: hashed_password column does not exist in user table!")

if __name__ == "__main__":
    reset_database()