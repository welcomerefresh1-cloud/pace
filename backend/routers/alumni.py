from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from core.database import get_session
from models.users import User, UserType
from models.degrees import Degree
from models.student_records import StudentRecord
from models.alumni import Alumni, AlumniCreate, AlumniPublic
from models.composite import CompleteAlumniRegistration, CompleteAlumniResponse
from models.responses import AlumniFullProfile
from models.errors import ErrorCode

router = APIRouter(prefix="/alumni", tags=["alumni"])


@router.post("/register", response_model=CompleteAlumniResponse)
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
            raise HTTPException(
                status_code=404,
                detail={
                    "code": ErrorCode.DEGREE_NOT_FOUND.value,
                    "message": f"Degree with ID '{data.degree_id}' not found"
                }
            )
        
        #generate user_id based
        user_type = UserType.USER
        last_user = session.exec(
            select(User).where(User.user_type == user_type).order_by(User.user_id.desc())
        ).first()
        
        #auto increment user_id
        if last_user:
            last_num = int(last_user.user_id.split("-")[1])
            new_num = last_num + 1
        else:
            new_num = 1
        
        user_id = f"USER-{new_num:06d}"  # Format: USER-000001
        
        #generate alumni_id
        last_alumni = session.exec(
            select(Alumni).order_by(Alumni.alumni_id.desc())
        ).first()
        
        #auto increment alumni_id
        if last_alumni and last_alumni.alumni_id.startswith("ALMN-"):
            last_alumni_num = int(last_alumni.alumni_id.split("-")[1])
            new_alumni_num = last_alumni_num + 1
        else:
            new_alumni_num = 1
        
        alumni_id = f"ALMN-{new_alumni_num:06d}"  # Format: ALMN-000001
        
        # Step 1: Create User
        new_user = User(
            user_id=user_id,
            username=data.username,
            email=data.email,
            password=data.password,  # TODO: Hash this
            user_type=UserType.USER
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
            user_id=new_user.user_id,
            student_id=new_student.student_id,
            alumni_id=new_alumni.alumni_id,
            message="Alumni profile created successfully"
        )
        
    except IntegrityError as e:
        session.rollback()
        error_str = str(e).lower()
        # Check which field caused the violation by looking at constraint name
        if "ix_users_email" in error_str or "users_email_key" in error_str:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": ErrorCode.DUPLICATE_EMAIL.value,
                    "message": "Email already in use"
                }
            )
        elif "ix_users_username" in error_str or "users_username_key" in error_str:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": ErrorCode.DUPLICATE_USERNAME.value,
                    "message": "Username already in use"
                }
            )
        elif "ix_student_records_student_id" in error_str or "student_records_student_id_key" in error_str:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": ErrorCode.DUPLICATE_STUDENT_ID.value,
                    "message": "Student ID already in use"
                }
            )
        elif "ix_alumni_alumni_id" in error_str or "alumni_alumni_id_key" in error_str:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": ErrorCode.DUPLICATE_ALUMNI_ID.value,
                    "message": "Alumni ID already in use"
                }
            )
        else:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": ErrorCode.REGISTRATION_FAILED.value,
                    "message": "Registration failed: Duplicate entry"
                }
            )
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=400,
            detail={
                "code": ErrorCode.REGISTRATION_FAILED.value,
                "message": f"Registration failed: {str(e)}"
            }
        )


@router.get("", response_model=list[AlumniFullProfile])
def get_all_alumni(session: Session = Depends(get_session)):
    """Get all alumni records with full profile information"""
    alumni_list = session.exec(select(Alumni)).all()
    
    result = []
    for alumni in alumni_list:
        # Get related student record
        student = session.exec(
            select(StudentRecord).where(StudentRecord.student_code == alumni.student_code)
        ).first()
        
        # Get related degree
        degree = session.exec(
            select(Degree).where(Degree.degree_code == student.degree_code)
        ).first()
        
        # Get related user (if exists)
        user = None
        if alumni.user_code:
            user = session.exec(
                select(User).where(User.user_code == alumni.user_code)
            ).first()
        
        # Build full profile
        profile = AlumniFullProfile(
            alumni_id=alumni.alumni_id,
            last_name=alumni.last_name,
            first_name=alumni.first_name,
            middle_name=alumni.middle_name,
            gender=alumni.gender,
            age=alumni.age,
            user_id=user.user_id if user else None,
            username=user.username if user else None,
            email=user.email if user else None,
            student_id=student.student_id,
            year_graduated=student.year_graduated,
            gwa=student.gwa,
            avg_prof_grade=student.avg_prof_grade,
            avg_elec_grade=student.avg_elec_grade,
            ojt_grade=student.ojt_grade,
            leadership_pos=student.leadership_pos,
            act_member_pos=student.act_member_pos,
            degree_id=degree.degree_id,
            degree_name=degree.degree_name,
            created_at=alumni.created_at,
            updated_at=alumni.updated_at
        )
        result.append(profile)
    
    return result


@router.get("/{alumni_id}", response_model=AlumniFullProfile)
def get_alumni(alumni_id: str, session: Session = Depends(get_session)):
    """Get specific alumni by alumni_id with full profile"""
    alumni = session.exec(
        select(Alumni).where(Alumni.alumni_id == alumni_id)
    ).first()
    
    if not alumni:
        raise HTTPException(
            status_code=404,
            detail={
                "code": ErrorCode.ALUMNI_NOT_FOUND.value,
                "message": "Alumni not found"
            }
        )
    
    # Get related student record
    student = session.exec(
        select(StudentRecord).where(StudentRecord.student_code == alumni.student_code)
    ).first()
    
    # Get related degree
    degree = session.exec(
        select(Degree).where(Degree.degree_code == student.degree_code)
    ).first()
    
    # Get related user (if exists)
    user = None
    if alumni.user_code:
        user = session.exec(
            select(User).where(User.user_code == alumni.user_code)
        ).first()
    
    # Build full profile
    return AlumniFullProfile(
        alumni_id=alumni.alumni_id,
        last_name=alumni.last_name,
        first_name=alumni.first_name,
        middle_name=alumni.middle_name,
        gender=alumni.gender,
        age=alumni.age,
        user_id=user.user_id if user else None,
        username=user.username if user else None,
        email=user.email if user else None,
        student_id=student.student_id,
        year_graduated=student.year_graduated,
        gwa=student.gwa,
        avg_prof_grade=student.avg_prof_grade,
        avg_elec_grade=student.avg_elec_grade,
        ojt_grade=student.ojt_grade,
        leadership_pos=student.leadership_pos,
        act_member_pos=student.act_member_pos,
        degree_id=degree.degree_id,
        degree_name=degree.degree_name,
        created_at=alumni.created_at,
        updated_at=alumni.updated_at
    )
