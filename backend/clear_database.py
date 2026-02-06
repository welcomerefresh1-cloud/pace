"""
Script to clear all data from the database.
Use with caution - this will delete ALL records!
"""
from sqlmodel import Session, select
from core.database import engine
from models import User, Degree, StudentRecord, Alumni, Skills, SkillsList


def clear_all_data():
    """Delete all records from all tables in the correct order."""
    
    print("⚠️  WARNING: This will delete ALL data from the database!")
    print("Tables to be cleared:")
    print("  - SkillsList")
    print("  - Skills")
    print("  - Alumni")
    print("  - StudentRecord")
    print("  - User")
    print("  - Degree")
    
    confirm = input("\nType 'DELETE ALL' to confirm: ")
    
    if confirm != "DELETE ALL":
        print("❌ Operation cancelled.")
        return
    
    with Session(engine) as session:
        try:
            # Delete in reverse order of dependencies (child tables first)
            
            # 1. Delete SkillsList (references Skills)
            skills_list_records = session.exec(select(SkillsList)).all()
            for record in skills_list_records:
                session.delete(record)
            print(f"✓ Deleted {len(skills_list_records)} records from SkillsList")
            
            # 2. Delete Skills (references Alumni)
            skills_records = session.exec(select(Skills)).all()
            for record in skills_records:
                session.delete(record)
            print(f"✓ Deleted {len(skills_records)} records from Skills")
            
            # 3. Delete Alumni (references User and StudentRecord)
            alumni_records = session.exec(select(Alumni)).all()
            for record in alumni_records:
                session.delete(record)
            print(f"✓ Deleted {len(alumni_records)} records from Alumni")
            
            # 4. Delete StudentRecord (references Degree)
            student_records = session.exec(select(StudentRecord)).all()
            for record in student_records:
                session.delete(record)
            print(f"✓ Deleted {len(student_records)} records from StudentRecord")
            
            # 5. Delete User
            user_records = session.exec(select(User)).all()
            for record in user_records:
                session.delete(record)
            print(f"✓ Deleted {len(user_records)} records from User")
            
            # 6. Delete Degree
            degree_records = session.exec(select(Degree)).all()
            for record in degree_records:
                session.delete(record)
            print(f"✓ Deleted {len(degree_records)} records from Degree")
            
            # Commit all deletions
            session.commit()
            print("\n✅ All data has been successfully deleted!")
            
        except Exception as e:
            session.rollback()
            print(f"\n❌ Error occurred: {str(e)}")
            print("Changes have been rolled back.")


if __name__ == "__main__":
    clear_all_data()
