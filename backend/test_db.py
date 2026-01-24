import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.config import settings
from src.core.database import engine
from src.models.user import User, UserBase
from sqlmodel import SQLModel, select
from sqlalchemy import inspect

def test_db_connection():
    print(f"Database URL: {settings.database_url}")

    # Check if the database file exists
    db_path = settings.database_url.replace("sqlite:///", "")
    print(f"Database file path: {db_path}")

    # Create tables
    print("Creating tables...")
    SQLModel.metadata.create_all(engine)
    print("Tables created successfully!")

    # Check the database structure
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"Tables in database: {tables}")

    if 'user' in tables:
        columns = inspector.get_columns('user')
        print("Columns in 'user' table:")
        for col in columns:
            print(f"  - {col['name']}: {col['type']} (nullable: {col['nullable']})")

    if 'task' in tables:
        columns = inspector.get_columns('task')
        print("Columns in 'task' table:")
        for col in columns:
            print(f"  - {col['name']}: {col['type']} (nullable: {col['nullable']})")

if __name__ == "__main__":
    test_db_connection()