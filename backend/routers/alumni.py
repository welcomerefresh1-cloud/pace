from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from core.database import get_session
from models.users import User, UserType
from models.degrees import Degree
from models.student_records import StudentRecord
from models.alumni import Alumni, AlumniCreate, AlumniUpdate, AlumniPublic
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
    2. Create Alumni profile (linked to User)
    
    Student record can be created separately via POST /student-records
    This ensures data integrity - if any step fails, nothing is saved.
    """
    try:
        # Generate user_id based on user_type
        user_type = UserType.USER
        last_user = session.exec(
            select(User).where(User.user_type == user_type).order_by(User.user_id.desc())
        ).first()
        
        # Auto increment user_id
        if last_user:
            last_num = int(last_user.user_id.split("-")[1])
            new_num = last_num + 1
        else:
            new_num = 1
        
        user_id = f"USER-{new_num:06d}"  # Format: USER-000001
        
        # Generate alumni_id
        last_alumni = session.exec(
            select(Alumni).order_by(Alumni.alumni_id.desc())
        ).first()
        
        # Auto increment alumni_id
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
        
        # Step 2: Create Alumni (linked to User, without student_code)
        new_alumni = Alumni(
            alumni_id=alumni_id,
            last_name=data.last_name,
            first_name=data.first_name,
            middle_name=data.middle_name,
            gender=data.gender,
            age=data.age,
            user_code=new_user.user_code
        )
        session.add(new_alumni)
        
        # Commit everything at once
        session.commit()
        
        return CompleteAlumniResponse(
            user_id=new_user.user_id,
            alumni_id=new_alumni.alumni_id,
            message="Alumni profile created successfully"
        )
        
    except IntegrityError as e:
        session.rollback()
        error_str = str(e).lower()
        print(f"DEBUG IntegrityError: {str(e)}")  # Log the actual error
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
                    "message": f"Registration failed: {str(e)}"
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
        # Get related student record (optional)
        student = None
        degree = None
        if alumni.student_code:
            student = session.exec(
                select(StudentRecord).where(StudentRecord.student_code == alumni.student_code)
            ).first()
            
            # Get related degree (only if student exists)
            if student:
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
            student_id=student.student_id if student else None,
            year_graduated=student.year_graduated if student else None,
            gwa=student.gwa if student else None,
            avg_prof_grade=student.avg_prof_grade if student else None,
            avg_elec_grade=student.avg_elec_grade if student else None,
            ojt_grade=student.ojt_grade if student else None,
            leadership_pos=student.leadership_pos if student else None,
            act_member_pos=student.act_member_pos if student else None,
            degree_id=degree.degree_id if degree else None,
            degree_name=degree.degree_name if degree else None,
            created_at=alumni.created_at,
            updated_at=alumni.updated_at
        )
        result.append(profile)
    
    return result


@router.get("/{alumni_id}", response_model=AlumniFullProfile)
def get_alumni(alumni_id: str, session: Session = Depends(get_session)):
    """Get specific alumni by alumni_id with full profile"""
    alumni = session.exec(
        select(Alumni).where(Alumni.alumni_id == alumni_id.upper())
    ).first()
    
    if not alumni:
        raise HTTPException(
            status_code=404,
            detail={
                "code": ErrorCode.ALUMNI_NOT_FOUND.value,
                "message": "Alumni not found"
            }
        )
    
    # Get related student record (optional)
    student = None
    degree = None
    if alumni.student_code:
        student = session.exec(
            select(StudentRecord).where(StudentRecord.student_code == alumni.student_code)
        ).first()
        
        # Get related degree (only if student exists)
        if student:
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
        student_id=student.student_id if student else None,
        year_graduated=student.year_graduated if student else None,
        gwa=student.gwa if student else None,
        avg_prof_grade=student.avg_prof_grade if student else None,
        avg_elec_grade=student.avg_elec_grade if student else None,
        ojt_grade=student.ojt_grade if student else None,
        leadership_pos=student.leadership_pos if student else None,
        act_member_pos=student.act_member_pos if student else None,
        degree_id=degree.degree_id if degree else None,
        degree_name=degree.degree_name if degree else None,
        created_at=alumni.created_at,
        updated_at=alumni.updated_at
    )


@router.put("/{alumni_id}", response_model=AlumniFullProfile)
def update_alumni(
    alumni_id: str,
    alumni_data: AlumniUpdate,
    session: Session = Depends(get_session)
):
    """Update alumni information"""
    alumni = session.exec(
        select(Alumni).where(Alumni.alumni_id == alumni_id.upper())
    ).first()
    
    if not alumni:
        raise HTTPException(
            status_code=404,
            detail={
                "code": ErrorCode.ALUMNI_NOT_FOUND.value,
                "message": "Alumni not found"
            }
        )
    
    # Update only provided fields
    if alumni_data.last_name is not None:
        alumni.last_name = alumni_data.last_name
    if alumni_data.first_name is not None:
        alumni.first_name = alumni_data.first_name
    if alumni_data.middle_name is not None:
        alumni.middle_name = alumni_data.middle_name
    if alumni_data.gender is not None:
        alumni.gender = alumni_data.gender.upper()
    if alumni_data.age is not None:
        alumni.age = alumni_data.age
    
    session.add(alumni)
    
    try:
        session.commit()
        session.refresh(alumni)
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(
            status_code=400,
            detail={
                "code": ErrorCode.INVALID_INPUT.value,
                "message": "Update failed: Invalid input or duplicate entry"
            }
        )
    
    # Fetch full profile for response
    student = None
    degree = None
    if alumni.student_code:
        student = session.exec(
            select(StudentRecord).where(StudentRecord.student_code == alumni.student_code)
        ).first()
        
        if student:
            degree = session.exec(
                select(Degree).where(Degree.degree_code == student.degree_code)
            ).first()
    
    user = None
    if alumni.user_code:
        user = session.exec(
            select(User).where(User.user_code == alumni.user_code)
        ).first()
    
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
        student_id=student.student_id if student else None,
        year_graduated=student.year_graduated if student else None,
        gwa=student.gwa if student else None,
        avg_prof_grade=student.avg_prof_grade if student else None,
        avg_elec_grade=student.avg_elec_grade if student else None,
        ojt_grade=student.ojt_grade if student else None,
        leadership_pos=student.leadership_pos if student else None,
        act_member_pos=student.act_member_pos if student else None,
        degree_id=degree.degree_id if degree else None,
        degree_name=degree.degree_name if degree else None,
        created_at=alumni.created_at,
        updated_at=alumni.updated_at
    )


@router.delete("/{alumni_id}")
def delete_alumni(alumni_id: str, session: Session = Depends(get_session)):
    """Delete an alumni record"""
    alumni = session.exec(
        select(Alumni).where(Alumni.alumni_id == alumni_id.upper())
    ).first()
    
    if not alumni:
        raise HTTPException(
            status_code=404,
            detail={
                "code": ErrorCode.ALUMNI_NOT_FOUND.value,
                "message": "Alumni not found"
            }
        )
    
    session.delete(alumni)
    session.commit()
    
    return {
        "message": f"Alumni {alumni_id} deleted successfully"
    }
