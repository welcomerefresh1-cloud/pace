from typing import Optional
from sqlmodel import Session, select, func, or_
from models.job_listings import JobListing

def _get_facet_counts(session: Session, keywords: Optional[str], location: Optional[str]) -> dict:
    """
    Helper to fetch facet counts from DB based on current search criteria (ignoring specific facet filters).
    """
    # Helper to build facet query
    def get_facet_query(group_col):
        q = select(group_col, func.count(JobListing.id)).where(JobListing.is_active == True)
        if keywords:
            search_term = f"%{keywords}%"
            q = q.where(
            or_(
                JobListing.title.ilike(search_term),
                JobListing.description.ilike(search_term),
                JobListing.company.ilike(search_term)
            )
            )
        if location and location != "Philippines":
            q = q.where(JobListing.location.ilike(f"%{location}%"))
        return q.group_by(group_col)

    # 1. Job Type Counts
    try:
        job_type_results = session.exec(get_facet_query(JobListing.job_type)).all()
        job_type_counts = {r[0]: r[1] for r in job_type_results if r[0]}
    except Exception as e:
        print(f"Error fetching job type facets: {e}")
        job_type_counts = {}

    # 2. Work Type Counts
    try:
        work_type_results = session.exec(get_facet_query(JobListing.work_type)).all()
        work_type_counts = {str(r[0]): r[1] for r in work_type_results if r[0]}
    except Exception as e:
        print(f"Error fetching work type facets: {e}")
        work_type_counts = {}

    # 3. Experience Level Counts
    try:
        exp_level_results = session.exec(get_facet_query(JobListing.experience_level)).all()
        experience_counts = {str(r[0]): r[1] for r in exp_level_results if r[0]}
    except Exception as e:
        print(f"Error fetching experience facets: {e}")
        experience_counts = {}
    
    return {
        "jobTypes": job_type_counts,
        "workTypes": work_type_counts,
        "experienceLevels": experience_counts
    }
