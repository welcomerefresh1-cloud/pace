"""
Script to clear all data from the database.
Use with caution - this will delete ALL records!

Run with: python scripts/clear_database.py
"""
from sqlmodel import Session, select
import sys
from pathlib import Path

# Add parent directory to path so we can import from backend modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.database import engine
from models.users import User
from models.degrees import Degree
from models.student_records import StudentRecord
from models.alumni import Alumni
from models.skills import Skills, SkillsList


# Define deletion order (child tables first, respecting foreign keys)
DELETION_ORDER = [
    (SkillsList, "SkillsList"),
    (Skills, "Skills"),
    (Alumni, "Alumni"),
    (StudentRecord, "StudentRecord"),
    (User, "User"),
    (Degree, "Degree"),
]


def clear_all_data():
    """Delete all records from all tables in the correct order."""
    
    print("⚠️  WARNING: This will delete ALL data from the database!")
    print("\nTables to be cleared (in order):")
    for model, name in DELETION_ORDER:
        print(f"  - {name}")
    
    confirm = input("\nType 'DELETE ALL' to confirm: ")
    
    if confirm != "DELETE ALL":
        print("❌ Operation cancelled.")
        return
    
    with Session(engine) as session:
        try:
            # Delete records in the defined order
            for model, name in DELETION_ORDER:
                records = session.exec(select(model)).all()
                for record in records:
                    session.delete(record)
                print(f"✓ Deleted {len(records)} records from {name}")
            
            # Commit all deletions
            session.commit()
            print("\n✅ All data has been successfully deleted!")
            
        except Exception as e:
            session.rollback()
            print(f"\n❌ Error occurred: {str(e)}")
            print("Changes have been rolled back.")


if __name__ == "__main__":
    clear_all_data()
