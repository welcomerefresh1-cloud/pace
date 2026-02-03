from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from core.database import get_session
from models.users import User, UserCreate, UserPublic
from models.degrees import Degree, DegreeCreate, DegreePublic
from models.student_records import StudentRecord, StudentRecordCreate, StudentRecordPublic
from models.alumni import Alumni, AlumniCreate, AlumniPublic
from models.composite import CompleteAlumniRegistration, CompleteAlumniResponse

app = FastAPI(
    title="Pasig Alumni and Career Employment (PACE) System",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Hello from PACE Backend"}


# COMPOSITE ENDPOINT - Create everything at once
@app.post("/alumni/register", response_model=CompleteAlumniResponse)
def register_complete_alumni(
    data: CompleteAlumniRegistration,
    session: Session = Depends(get_session)
):
    """
    Create a complete alumni profile in one transaction:
    1. Create User account
    2. Create Student Record (using user's UUID)
    3. Create Alumni profile (using both UUIDs)
    
    This ensures data integrity - if any step fails, nothing is saved.
    """
    try:
        # Verify degree exists by degree_id
        degree = session.exec(
            select(Degree).where(Degree.degree_id == data.degree_id)
        ).first()
        if not degree:
            raise HTTPException(status_code=404, detail=f"Degree with ID '{data.degree_id}' not found")
        
        # Generate sequential user_id for normal users (USER-XXXXXX)
        last_user = session.exec(
            select(User).where(User.user_id.like("USER-%")).order_by(User.user_id.desc())
        ).first()
        
        if last_user:
            # Extract number and increment
            last_num = int(last_user.user_id.split("-")[1])
            new_num = last_num + 1
        else:
            # Start from 1 if no users exist
            new_num = 1
        
        user_id = f"USER-{new_num:06d}"  # Format: USER-000001
        
        # Generate sequential alumni_id (ALMN-XXXXXX)
        last_alumni = session.exec(
            select(Alumni).order_by(Alumni.alumni_id.desc())
        ).first()
        
        if last_alumni and last_alumni.alumni_id.startswith("ALMN-"):
            # Extract number and increment
            last_alumni_num = int(last_alumni.alumni_id.split("-")[1])
            new_alumni_num = last_alumni_num + 1
        else:
            # Start from 1 if no alumni exist
            new_alumni_num = 1
        
        alumni_id = f"ALMN-{new_alumni_num:06d}"  # Format: ALMN-000001
        
        # Step 1: Create User
        new_user = User(
            user_id=user_id,
            username=data.username,
            email=data.email,
            password=data.password  # TODO: Hash this
        )
        session.add(new_user)
        session.flush()  # Get UUID without committing
        
        # Step 2: Create Student Record (using user's UUID)
        new_student = StudentRecord(
            student_id=data.student_id,
            year_graduated=data.year_graduated,
            gwa=data.gwa,
            avg_prof_grade=data.avg_prof_grade,
            avg_elec_grade=data.avg_elec_grade,
            ojt_grade=data.ojt_grade,
            leadership_pos=data.leadership_pos,
            act_member_pos=data.act_member_pos,
            degree_code=degree.degree_code
        )
        session.add(new_student)
        session.flush()  # Get UUID without committing
        
        # Step 3: Create Alumni (using both UUIDs and generated alumni_id)
        new_alumni = Alumni(
            alumni_id=alumni_id,
            last_name=data.last_name,
            first_name=data.first_name,
            middle_name=data.middle_name,
            gender=data.gender,
            age=data.age,
            user_code=new_user.user_code,
            student_code=new_student.student_code
        )
        session.add(new_alumni)
        
        # Commit everything at once
        session.commit()
        
        return CompleteAlumniResponse(
            user_code=new_user.user_code,
            student_code=new_student.student_code,
            alumni_code=new_alumni.alumni_code,
            message="Alumni profile created successfully"
        )
        
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Registration failed: {str(e)}")


# Step 1: Create User
@app.post("/users", response_model=UserPublic)
def create_user(
    user_data: UserCreate,
    session: Session = Depends(get_session)
):
    """Create a new user account"""
    # TODO: Hash password before storing (add bcrypt later)
    new_user = User.model_validate(user_data)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@app.get("/users", response_model=list[UserPublic])
def get_all_users(session: Session = Depends(get_session)):
    """Get all users"""
    users = session.exec(select(User)).all()
    return users


# Step 2: Create/Get Degree
@app.post("/degrees", response_model=DegreePublic)
def create_degree(
    degree_data: DegreeCreate,
    session: Session = Depends(get_session)
):
    """Create a new degree program"""
    new_degree = Degree.model_validate(degree_data)
    session.add(new_degree)
    session.commit()
    session.refresh(new_degree)
    return new_degree


@app.get("/degrees", response_model=list[DegreePublic])
def get_all_degrees(session: Session = Depends(get_session)):
    """Get all degree programs"""
    degrees = session.exec(select(Degree)).all()
    return degrees


# READ-ONLY endpoints for Student Records
@app.get("/student-records", response_model=list[StudentRecordPublic])
def get_all_student_records(session: Session = Depends(get_session)):
    """Get all student records"""
    students = session.exec(select(StudentRecord)).all()
    return students


# READ-ONLY endpoints for Alumni
@app.get("/alumni", response_model=list[AlumniPublic])
def get_all_alumni(session: Session = Depends(get_session)):
    """Get all alumni records"""
    alumni = session.exec(select(Alumni)).all()
    return alumni


@app.get("/alumni/{alumni_id}", response_model=AlumniPublic)
def get_alumni(alumni_id: str, session: Session = Depends(get_session)):
    """Get specific alumni by alumni_id"""
    alumni = session.exec(
        select(Alumni).where(Alumni.alumni_id == alumni_id)
    ).first()
    
    if not alumni:
        raise HTTPException(status_code=404, detail="Alumni not found")
    
    return alumni
