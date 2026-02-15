import httpx
import math
import asyncio 
import traceback
import httpx
import math
import asyncio 
import traceback
from typing import Optional
from datetime import datetime, timedelta

from sqlmodel import Session, select, col, or_, func
from core.config import settings
from core.database import engine
from core.redis import cache_get, cache_set, generate_cache_key, cache_invalidate_job_searches, cache_invalidate_recommended
from models.job_listings import JobListing
from fastapi import BackgroundTasks

from .constants import JOOBLE_API_URL, JOOBLE_BATCH_SIZE
from .facets import _get_facet_counts
from .normalization import _normalize_job_dict
from .mappers import _map_db_job_to_dict

def load_all_jobs_to_cache(session: Session) -> int:
    """
    Load all active jobs from database into Redis cache.
    Called on app startup and periodically to refresh the bulk cache.
    
    Returns:
        Number of jobs cached
    """
    try:
        query = select(JobListing).where(JobListing.is_active == True)
        all_jobs = session.exec(query).all()
        
        # Convert to dict format
        jobs_data = [_map_db_job_to_dict(job) for job in all_jobs]
        
        # Cache for 6 hours
        from core.redis import cache_set_all_jobs
        cache_set_all_jobs(jobs_data, ttl=21600)
        
        return len(jobs_data)
    except Exception as e:
        print(f"[ERROR] Failed to load jobs to cache: {e}")
        return 0

def get_recommended_jobs(session: Session, limit: int = 3) -> list[dict]:
    """
    Get recommended jobs from the database cache.
    Currently returns random active jobs.
    Uses Redis caching to avoid repeated database queries.
    """
    # Generate cache key
    cache_key = generate_cache_key("recommended_jobs", limit=limit)
    
    # 1. Check Redis cache first
    cached_result = cache_get(cache_key)
    if cached_result is not None:
        return cached_result
    
    # 2. Fall back to database query
    query = select(JobListing).where(JobListing.is_active == True).order_by(func.random()).limit(limit)
    jobs = session.exec(query).all()
    result = [_map_db_job_to_dict(job) for job in jobs]
    
    # 3. Cache the result (1 hour TTL)
    cache_set(cache_key, result, ttl=3600)
    
    return result


async def fetch_jobs(
    keywords: Optional[str] = None,
    location: Optional[str] = "Philippines",
    job_type: Optional[str] = None,
    work_type: Optional[str] = None,
    experience_level: Optional[str] = None,
    page: int = 1,
    results_per_page: int = 10,
    salary: Optional[int] = None,
    # dependency injection for database session will be passed by the router
    session: Optional['Session'] = None,
    background_tasks: Optional['BackgroundTasks'] = None,
    has_salary: bool = False
) -> dict:
    """
    Fetch job listings from Jooble API for the Philippines.
    Uses bulk Redis cache for instant filtering.
    
    Args:
        keywords: Search keywords for job title/description
        location: Location filter (defaults to Philippines)
        job_type: Job type filter (Full-time, Part-time, etc.)
        work_type: Work type filter (On-site, Remote, etc.)
        experience_level: Experience level filter (Senior, Junior, etc.)
        page: Page number for pagination
        results_per_page: Number of results per page
        salary: Minimum salary filter
        session: Database session for caching
        background_tasks: FastAPI BackgroundTasks for fetching remaining jobs
    
    Returns:
        dict: Contains 'jobs' list and 'totalCount' of available jobs
    """
    print(f"\n[FETCH_JOBS] Searching: keywords={keywords}, location={location}, job_type={job_type}, work_type={work_type}, experience_level={experience_level}, page={page}")
    
    # Try bulk cache first
    from core.redis import cache_get_all_jobs
    all_cached_jobs = cache_get_all_jobs()
    
    if all_cached_jobs is not None:
        print(f"[FETCH_JOBS] Using bulk cache ({len(all_cached_jobs)} total jobs)")
        
        # Filter jobs in-memory
        filtered_jobs = all_cached_jobs
        
        # Apply filters
        if keywords:
            search_lower = keywords.lower()
            filtered_jobs = [
                j for j in filtered_jobs 
                if search_lower in j.get('title', '').lower() 
                or search_lower in j.get('company', '').lower()
                or search_lower in j.get('description', '').lower()
            ]
        
        if location and location != "Philippines":
            filtered_jobs = [
                j for j in filtered_jobs 
                if location.lower() in j.get('location', '').lower()
            ]
        
        if job_type:
            job_type_lower = job_type.lower()
            filtered_jobs = [
                j for j in filtered_jobs 
                if job_type_lower in j.get('type', '').lower()  # Use 'type' not 'job_type'
            ]
        
        if work_type:
            work_type_lower = work_type.lower()
            filtered_jobs = [
                j for j in filtered_jobs 
                if work_type_lower in j.get('work_type', '').lower()
            ]
        
        if experience_level:
            exp_level_lower = experience_level.lower()
            filtered_jobs = [
                j for j in filtered_jobs 
                if exp_level_lower in j.get('experience_level', '').lower()
            ]
        
        if has_salary:
            filtered_jobs = [
                j for j in filtered_jobs 
                if any(char.isdigit() for char in j.get('salary', ''))
            ]
        
        # Paginate
        total_count = len(filtered_jobs)
        start_idx = (page - 1) * results_per_page
        end_idx = start_idx + results_per_page
        paginated_jobs = filtered_jobs[start_idx:end_idx]
        
        print(f"[FETCH_JOBS] ✓ Bulk cache hit! Filtered {len(paginated_jobs)} results from {total_count} matching jobs")
        
        return {
            "jobs": paginated_jobs,
            "totalCount": total_count,
            "facets": _get_facet_counts(session, keywords, location) if session else {}
        }
    
    # Fallback to original logic if bulk cache miss
    print(f"[FETCH_JOBS] Bulk cache miss, falling back to API/DB fetch")
    
    # Generate Redis cache key based on search parameters
    cache_key = generate_cache_key(
        "job_search",
        keywords=keywords,
        location=location,
        job_type=job_type,
        work_type=work_type,
        experience_level=experience_level,
        page=page,
        results_per_page=results_per_page,
        salary=salary,
        has_salary=has_salary
    )
    
    # Check direct cache for this specific query
    from core.redis import cache_get
    cached_result = cache_get(cache_key)
    if cached_result is not None:
        print(f"[FETCH_JOBS] ✓ Direct cache hit! Returning cached results")
        return cached_result
    print(f"[FETCH_JOBS] Direct cache miss, checking database...")
    
    # Normalize location
    search_location = location
    if location and location != "Philippines" and "philippines" not in location.lower():
         search_location = f"{location}, Philippines"
    
    # Attempt to fetch from DB Cache if session available
    if session:
        # Build base query
        query = select(JobListing).where(JobListing.is_active == True)
        
        # Apply filters to DB query
        if keywords:
            search_term = f"%{keywords}%"
            query = query.where(
                or_(
                    JobListing.title.ilike(search_term),
                    JobListing.description.ilike(search_term),
                    JobListing.company.ilike(search_term)
                )
            )
        
        if location and location != "Philippines":
             query = query.where(JobListing.location.ilike(f"%{location}%"))
        
        # Job Type Filter
        if job_type:
             query = query.where(JobListing.job_type.ilike(f"%{job_type}%"))
        
        # Has Salary Filter
        if has_salary:
            query = query.where(JobListing.raw_salary != None).where(JobListing.raw_salary != "").where(JobListing.raw_salary != "Negotiable")
        
        user_offset = (page - 1) * results_per_page
        query_slice = query.offset(user_offset).limit(results_per_page)
        
        cached_jobs_raw = session.exec(query_slice).all()
        
        # FILTER IN PYTHON for cached jobs (since SQL regex support varies)
        if has_salary:
             cached_jobs = [j for j in cached_jobs_raw if any(char.isdigit() for char in (j.raw_salary or ""))]
        else:
             cached_jobs = cached_jobs_raw
        
        should_fetch_api = False
        if len(cached_jobs) < results_per_page:
            should_fetch_api = True

        if not should_fetch_api and len(cached_jobs) >= results_per_page:
             print(f"[FETCH_JOBS] ✓ DB hit! Found {len(cached_jobs)} jobs in database")
             # Calculate actual total count matching the filters
             count_query = select(func.count(JobListing.id)).where(JobListing.is_active == True)
             if keywords:
                 count_query = count_query.where(
                    or_(
                        JobListing.title.ilike(f"%{keywords}%"),
                        JobListing.description.ilike(f"%{keywords}%"),
                        JobListing.company.ilike(f"%{keywords}%")
                    )
                 )
             if location and location != "Philippines":
                 count_query = count_query.where(JobListing.location.ilike(f"%{location}%"))
             if job_type:
                 count_query = count_query.where(JobListing.job_type.ilike(f"%{job_type}%"))
                 
             if has_salary:
                 count_query = count_query.where(JobListing.raw_salary != None).where(JobListing.raw_salary != "").where(JobListing.raw_salary != "Negotiable")

             total_count = session.exec(count_query).one()
             
             # --- FACET COUNTS ---
             facets = _get_facet_counts(session, keywords, location)
             
             result = {
                "jobs": [_map_db_job_to_dict(job) for job in cached_jobs],
                "totalCount": total_count,
                "facets": facets
             }
             
             # Cache this result
             cache_set(cache_key, result, ttl=3600)
             
             return result

    # 2. Fetch from API (Cache Miss)
    if not settings.JOOBLE_API_KEY or settings.JOOBLE_API_KEY == "your_api_key_here":
        return {
            "jobs": [],
            "totalCount": 0,
            "error": "Jooble API key not configured."
        }
    
    # Calculate API Page
    target_index = (page - 1) * results_per_page
    api_page = (target_index // JOOBLE_BATCH_SIZE) + 1
    
    # Construct keywords with job type to improve relevance
    api_keywords = keywords or ""
    if job_type:
        api_keywords = f"{api_keywords} {job_type}".strip()

    payload = {
        "keywords": api_keywords,
        "location": search_location or "Philippines",
        "page": str(api_page),
        "ResultOnPage": str(JOOBLE_BATCH_SIZE),
    }
    
    if salary:
        payload["salary"] = str(salary)
    
    fetch_start_time = datetime.utcnow()

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                JOOBLE_API_URL,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            data = response.json()
            
            # Normalize and Save to DB
            normalized_jobs = []
            for job in data.get("jobs", []):
                job_data = _normalize_job_dict(job)
                
                # OVERRIDE: If API returns generic "Philippines" but we searched for specific location, use that.
                if job_data["location"] == "Philippines" and search_location and search_location != "Philippines":
                     job_data["location"] = search_location

                # FILTER: Skip jobs with no numeric salary
                if has_salary and not any(char.isdigit() for char in job_data["salary"]):
                    continue
                    
                normalized_jobs.append(job_data)

                if session:
                    try:
                        external_id = job_data["id"]
                        existing_job = session.exec(select(JobListing).where(JobListing.external_id == external_id)).first()
                        
                        if not existing_job:
                            new_job = JobListing(
                                title=job_data["title"],
                                company=job_data["company"],
                                description=job_data["snippet"],
                                location=job_data["location"],
                                job_type=job_data["type"],
                                work_type=job_data["work_type"],
                                experience_level=job_data["experience_level"],
                                raw_salary=job_data["salary"],
                                source_api="Jooble",
                                external_id=external_id,
                                source_url=job_data["link"],
                                posted_at=datetime.utcnow(),
                                updated_at=datetime.utcnow()
                            )
                            session.add(new_job)
                        else:
                            existing_job.work_type = job_data["work_type"]
                            existing_job.experience_level = job_data["experience_level"]
                            existing_job.job_type = job_data["type"]
                            existing_job.raw_salary = job_data["salary"]
                            if job_data["location"] != "Philippines" and job_data["location"] != existing_job.location:
                                 existing_job.location = job_data["location"]
                            existing_job.title = job_data["title"]
                            existing_job.company = job_data["company"]
                            existing_job.description = job_data["snippet"]
                            existing_job.updated_at = datetime.utcnow()
                            session.add(existing_job)
                            
                    except Exception as db_e:
                        print(f"Error caching job {external_id}: {db_e}")
            
            if session:
                try:
                    session.commit()
                except Exception as commit_e:
                    print(f"Error committing cached jobs: {commit_e}")
            
            # TRIGGER BACKGROUND FETCH
            total_count = int(data.get("totalCount", 0))

            if background_tasks and api_page == 1 and total_count > JOOBLE_BATCH_SIZE:
                 background_tasks.add_task(
                     fetch_all_remaining_jobs, 
                     keywords=keywords, 
                     location=search_location, 
                     salary=salary,
                     start_page=2,
                     total_count=total_count,
                     fetch_start_time=fetch_start_time,
                     job_type=job_type,
                     has_salary=has_salary
                 )
            
            # Force Database Return to ensure consistency with filters
            if session:

                final_query = select(JobListing).where(JobListing.is_active == True)
                
                if keywords:
                    search_term = f"%{keywords}%"
                    final_query = final_query.where(
                        or_(
                            JobListing.title.ilike(search_term),
                            JobListing.description.ilike(search_term),
                            JobListing.company.ilike(search_term)
                        )
                    )
                
                if location and location != "Philippines":
                     final_query = final_query.where(JobListing.location.ilike(f"%{location}%"))
                
                if job_type:
                     final_query = final_query.where(JobListing.job_type.ilike(f"%{job_type}%"))
                     
                if has_salary:
                    final_query = final_query.where(JobListing.raw_salary != None).where(JobListing.raw_salary != "").where(JobListing.raw_salary != "Negotiable")
                
                count_query = select(func.count(JobListing.id)).where(JobListing.is_active == True)
                if keywords:
                    count_query = count_query.where(
                        or_(
                            JobListing.title.ilike(f"%{keywords}%"),
                            JobListing.description.ilike(f"%{keywords}%"),
                            JobListing.company.ilike(f"%{keywords}%")
                        )
                    )
                if location and location != "Philippines":
                    count_query = count_query.where(JobListing.location.ilike(f"%{location}%"))
                if job_type:
                    count_query = count_query.where(JobListing.job_type.ilike(f"%{job_type}%"))
                
                if has_salary:
                    count_query = count_query.where(JobListing.raw_salary != None).where(JobListing.raw_salary != "").where(JobListing.raw_salary != "Negotiable")

                total_count_db = session.exec(count_query).one()
                
                user_offset = (page - 1) * results_per_page
                query_slice = final_query.offset(user_offset).limit(results_per_page)
                db_jobs = session.exec(query_slice).all()
                
                result = {
                    "jobs": [_map_db_job_to_dict(job) for job in db_jobs],
                    "totalCount": total_count_db,
                    "facets": _get_facet_counts(session, keywords, location)
                }
                
                cache_set(cache_key, result, ttl=3600)
                
                return result

            batch_start_index = (api_page - 1) * JOOBLE_BATCH_SIZE
            req_start_index = (page - 1) * results_per_page
            req_end_index = req_start_index + results_per_page
            
            slice_start = max(0, req_start_index - batch_start_index)
            slice_end = min(len(normalized_jobs), req_end_index - batch_start_index)
            
            result_slice = normalized_jobs[slice_start:slice_end]
            
            result = {
                "jobs": result_slice,
                "totalCount": total_count
            }
            
            cache_set(cache_key, result, ttl=3600)
            
            return result
            
    except httpx.HTTPStatusError as e:
        return {
            "jobs": [],
            "totalCount": 0,
            "error": f"Jooble API error: {e.response.status_code}"
        }
    except httpx.RequestError as e:
        return {
            "jobs": [],
            "totalCount": 0,
            "error": f"Request failed: {str(e)}"
        }
    except Exception as e:
        traceback.print_exc()
        return {
            "jobs": [],
            "totalCount": 0,
            "error": f"Unexpected error: {str(e)}"
        }
    
    # Normalize location
    search_location = location
    if location and location != "Philippines" and "philippines" not in location.lower():
         search_location = f"{location}, Philippines"
    
    # 1. Attempt to fetch from DB Cache if session available
    if session:
        # Build base query
        query = select(JobListing).where(JobListing.is_active == True)
        
        # Apply filters to DB query
        if keywords:
            search_term = f"%{keywords}%"
            query = query.where(
                or_(
                    JobListing.title.ilike(search_term),
                    JobListing.description.ilike(search_term),
                    JobListing.company.ilike(search_term)
                )
            )
        
        if location and location != "Philippines":
             query = query.where(JobListing.location.ilike(f"%{location}%"))
        
        # Job Type Filter
        if job_type:
             query = query.where(JobListing.job_type.ilike(f"%{job_type}%"))
        
        # Salary filter (simple approximation for DB)
        if salary:
            pass 
            
        # Has Salary Filter
        if has_salary:
            query = query.where(JobListing.raw_salary != None).where(JobListing.raw_salary != "").where(JobListing.raw_salary != "Negotiable")
        
        user_offset = (page - 1) * results_per_page
        query_slice = query.offset(user_offset).limit(results_per_page)
        
        cached_jobs_raw = session.exec(query_slice).all()
        
        # FILTER IN PYTHON for cached jobs (since SQL regex support varies)
        if has_salary:
             cached_jobs = [j for j in cached_jobs_raw if any(char.isdigit() for char in (j.raw_salary or ""))]
        else:
             cached_jobs = cached_jobs_raw
        
        should_fetch_api = False
        if len(cached_jobs) < results_per_page:
            
            should_fetch_api = True
                 
        if cached_jobs and len(cached_jobs) > 0:
             # We rely on background workers or manual refreshes for updates now.
             # This prevents blocking the UI for a growing cache.
             pass

        if not should_fetch_api and len(cached_jobs) >= results_per_page:
             print(f"[FETCH_JOBS] ✓ DB hit! Found {len(cached_jobs)} jobs in database")
             # Calculate actual total count matching the filters
             # We use the same filters as the main query
             # Avoid subquery for count to prevent aliasing issues
             count_query = select(func.count(JobListing.id)).where(JobListing.is_active == True)
             if keywords:
                 count_query = count_query.where(
                    or_(
                        JobListing.title.ilike(f"%{keywords}%"),
                        JobListing.description.ilike(f"%{keywords}%"),
                        JobListing.company.ilike(f"%{keywords}%")
                    )
                 )
             if location and location != "Philippines":
                 count_query = count_query.where(JobListing.location.ilike(f"%{location}%"))
             if job_type:
                 count_query = count_query.where(JobListing.job_type.ilike(f"%{job_type}%"))
                 
             if has_salary:
                 count_query = count_query.where(JobListing.raw_salary != None).where(JobListing.raw_salary != "").where(JobListing.raw_salary != "Negotiable")

             total_count = session.exec(count_query).one()
             
             # --- FACET COUNTS ---
             facets = _get_facet_counts(session, keywords, location)
             
             result = {
                "jobs": [_map_db_job_to_dict(job) for job in cached_jobs],
                "totalCount": total_count,
                "facets": facets
             }
             
             # Cache this result in Redis (1 hour TTL)
             cache_set(cache_key, result, ttl=3600)
             
             return result

    # 2. Fetch from API (Cache Miss)
    if not settings.JOOBLE_API_KEY or settings.JOOBLE_API_KEY == "your_api_key_here":
        return {
            "jobs": [],
            "totalCount": 0,
            "error": "Jooble API key not configured."
        }
    
    # Calculate API Page
    target_index = (page - 1) * results_per_page
    api_page = (target_index // JOOBLE_BATCH_SIZE) + 1
    
    # Construct keywords with job type to improve relevance
    api_keywords = keywords or ""
    if job_type:
        api_keywords = f"{api_keywords} {job_type}".strip()

    payload = {
        "keywords": api_keywords,
        "location": search_location or "Philippines",
        "page": str(api_page),
        "ResultOnPage": str(JOOBLE_BATCH_SIZE), # Aggressive fetch
    }
    
    if salary:
        payload["salary"] = str(salary)
    
    fetch_start_time = datetime.utcnow()

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                JOOBLE_API_URL,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            data = response.json()
            
            # Normalize and Save to DB
            normalized_jobs = []
            for job in data.get("jobs", []):
                job_data = _normalize_job_dict(job)
                
                # OVERRIDE: If API returns generic "Philippines" but we searched for specific location, use that.
                if job_data["location"] == "Philippines" and search_location and search_location != "Philippines":
                     job_data["location"] = search_location

                # FILTER: Skip jobs with no numeric salary - REMOVED to fix pagination
                if has_salary and not any(char.isdigit() for char in job_data["salary"]):
                    continue
                    
                normalized_jobs.append(job_data)

                if session:
                    try:
                        external_id = job_data["id"]
                        existing_job = session.exec(select(JobListing).where(JobListing.external_id == external_id)).first()
                        
                        if not existing_job:
                            new_job = JobListing(
                                title=job_data["title"],
                                company=job_data["company"],
                                description=job_data["snippet"],
                                location=job_data["location"],
                                job_type=job_data["type"],
                                work_type=job_data["work_type"],
                                experience_level=job_data["experience_level"],
                                raw_salary=job_data["salary"],
                                source_api="Jooble",
                                external_id=external_id,
                                source_url=job_data["link"],
                                posted_at=datetime.utcnow(),
                                updated_at=datetime.utcnow()
                            )
                            session.add(new_job)
                        else:
                            existing_job.work_type = job_data["work_type"]
                            existing_job.experience_level = job_data["experience_level"]
                            existing_job.job_type = job_data["type"]
                            existing_job.raw_salary = job_data["salary"]
                            # Update location if it's more specific than "Philippines" or if it changed
                            if job_data["location"] != "Philippines" and job_data["location"] != existing_job.location:
                                 existing_job.location = job_data["location"]
                            # Also update title/company/description just in case
                            existing_job.title = job_data["title"]
                            existing_job.company = job_data["company"]
                            existing_job.description = job_data["snippet"]
                            existing_job.updated_at = datetime.utcnow()
                            session.add(existing_job)
                            
                    except Exception as db_e:
                        print(f"Error caching job {external_id}: {db_e}")
            
            if session:
                try:
                    session.commit()
                except Exception as commit_e:
                    print(f"Error committing cached jobs: {commit_e}")
            
            # TRIGGER BACKGROUND FETCH
            # If we just fetched Page 1, and there are more results than what we got,
            # we trigger the background task to get the rest.
            total_count = int(data.get("totalCount", 0))

            if background_tasks and api_page == 1 and total_count > JOOBLE_BATCH_SIZE:
                 background_tasks.add_task(
                     fetch_all_remaining_jobs, 
                     keywords=keywords, 
                     location=search_location, 
                     salary=salary,
                     start_page=2, # Since we just got Page 1
                     total_count=total_count,
                     fetch_start_time=fetch_start_time, # Pass the start time for consistency
                     job_type=job_type, # Pass job_type to background task
                     has_salary=has_salary
                 )
            
            # Force Database Return to ensure consistency with filters
            # We re-run the exact same query logic as the cache hit path
            if session:

                final_query = select(JobListing).where(JobListing.is_active == True)
                
                if keywords:
                    search_term = f"%{keywords}%"
                    final_query = final_query.where(
                        or_(
                            JobListing.title.ilike(search_term),
                            JobListing.description.ilike(search_term),
                            JobListing.company.ilike(search_term)
                        )
                    )
                
                if location and location != "Philippines":
                     final_query = final_query.where(JobListing.location.ilike(f"%{location}%"))
                
                if job_type:
                     final_query = final_query.where(JobListing.job_type.ilike(f"%{job_type}%"))
                     
                if has_salary:
                    final_query = final_query.where(JobListing.raw_salary != None).where(JobListing.raw_salary != "").where(JobListing.raw_salary != "Negotiable")
                
                # Fetch Count (No subquery)
                count_query = select(func.count(JobListing.id)).where(JobListing.is_active == True)
                if keywords:
                    count_query = count_query.where(
                        or_(
                            JobListing.title.ilike(f"%{keywords}%"),
                            JobListing.description.ilike(f"%{keywords}%"),
                            JobListing.company.ilike(f"%{keywords}%")
                        )
                    )
                if location and location != "Philippines":
                    count_query = count_query.where(JobListing.location.ilike(f"%{location}%"))
                if job_type:
                    count_query = count_query.where(JobListing.job_type.ilike(f"%{job_type}%"))
                
                if has_salary:
                    count_query = count_query.where(JobListing.raw_salary != None).where(JobListing.raw_salary != "").where(JobListing.raw_salary != "Negotiable")

                total_count_db = session.exec(count_query).one()
                
                # Fetch Page slice
                user_offset = (page - 1) * results_per_page
                query_slice = final_query.offset(user_offset).limit(results_per_page)
                db_jobs = session.exec(query_slice).all()
                
                result = {
                    "jobs": [_map_db_job_to_dict(job) for job in db_jobs],
                    "totalCount": total_count_db,
                    "facets": _get_facet_counts(session, keywords, location)
                }
                
                # Cache this result in Redis (1 hour TTL)
                cache_set(cache_key, result, ttl=3600)
                
                return result

            batch_start_index = (api_page - 1) * JOOBLE_BATCH_SIZE
            req_start_index = (page - 1) * results_per_page
            req_end_index = req_start_index + results_per_page
            
            slice_start = max(0, req_start_index - batch_start_index)
            slice_end = min(len(normalized_jobs), req_end_index - batch_start_index)
            
            result_slice = normalized_jobs[slice_start:slice_end]
            
            result = {
                "jobs": result_slice,
                "totalCount": total_count
            }
            
            # Cache this result in Redis (1 hour TTL)
            cache_set(cache_key, result, ttl=3600)
            
            return result
            
    except httpx.HTTPStatusError as e:
        return {
            "jobs": [],
            "totalCount": 0,
            "error": f"Jooble API error: {e.response.status_code}"
        }
    except httpx.RequestError as e:
        return {
            "jobs": [],
            "totalCount": 0,
            "error": f"Request failed: {str(e)}"
        }
    except Exception as e:
        traceback.print_exc()
        return {
            "jobs": [],
            "totalCount": 0,
            "error": f"Unexpected error: {str(e)}"
        }

async def fetch_all_remaining_jobs(
    keywords: Optional[str],
    location: Optional[str],
    salary: Optional[int],
    start_page: int,
    total_count: int,
    fetch_start_time: Optional[datetime] = None,
    job_type: Optional[str] = None,
    has_salary: bool = False
):

    
    MAX_JOBS_LIMIT = 1000
    
    if fetch_start_time is None:
        fetch_start_time = datetime.utcnow()

    real_limit = min(total_count, MAX_JOBS_LIMIT)
    total_pages = math.ceil(real_limit / JOOBLE_BATCH_SIZE)
    
    if start_page > total_pages:
        return

    print(f"Starting background fetch for {real_limit} jobs (Pages {start_page} to {total_pages})...")

    async with httpx.AsyncClient(timeout=30.0) as client:
        for p in range(start_page, total_pages + 1):
            try:
                # Small delay to be nice to API
                await asyncio.sleep(1.0)
                
                # Construct keywords with job type if passed
                api_keywords = keywords or ""
                if job_type:
                    api_keywords = f"{api_keywords} {job_type}".strip()

                payload = {
                    "keywords": api_keywords,
                    "location": location or "Philippines",
                    "page": str(p),
                    "ResultOnPage": str(JOOBLE_BATCH_SIZE),
                }
                if salary:
                    payload["salary"] = str(salary)
                
                response = await client.post(
                    JOOBLE_API_URL,
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code != 200:
                    print(f"Background fetch failed for page {p}: {response.status_code}")
                    continue
                    
                data = response.json()
                jobs = data.get("jobs", [])
                
                if not jobs:
                    break
                
                with Session(engine) as session:
                    saved_count = 0
                    for job in jobs:
                        try:
                            # NORMALIZE HERE
                            job_data = _normalize_job_dict(job)
                            
                            # OVERRIDE: If API returns generic "Philippines" but we searched for specific location, use that.
                            if job_data["location"] == "Philippines" and location and location != "Philippines":
                                 job_data["location"] = location
                            
                            external_id = job_data["id"]
                            
                            existing_job = session.exec(select(JobListing).where(JobListing.external_id == external_id)).first()
                            
                            if not existing_job:
                                new_job = JobListing(
                                    title=job_data["title"],
                                    company=job_data["company"],
                                    description=job_data["snippet"],
                                    location=job_data["location"],
                                    job_type=job_data["type"],
                                    work_type=job_data["work_type"],
                                    experience_level=job_data["experience_level"],
                                    raw_salary=job_data["salary"],
                                    source_api="Jooble",
                                    external_id=external_id,
                                    source_url=job_data["link"],
                                    posted_at=datetime.utcnow(),
                                    updated_at=datetime.utcnow(),
                                    is_active=True
                                )
                                session.add(new_job)
                            else:
                                existing_job.work_type = job_data["work_type"]
                                existing_job.experience_level = job_data["experience_level"]
                                existing_job.job_type = job_data["type"]
                                existing_job.raw_salary = job_data["salary"]
                                # Update location if it's more specific than "Philippines" or if it changed
                                if job_data["location"] != "Philippines" and job_data["location"] != existing_job.location:
                                     existing_job.location = job_data["location"]
                                # Also update title/company/description just in case
                                existing_job.title = job_data["title"]
                                existing_job.company = job_data["company"]
                                existing_job.description = job_data["snippet"]
                                existing_job.updated_at = datetime.utcnow()
                                session.add(existing_job)
                            
                            saved_count += 1

                        except Exception as e:
                            print(f"Error saving background job: {e}")
                    
                    session.commit()
                    print(f"Background fetch: Saved page {p} ({saved_count} jobs, filtered {len(jobs) - saved_count})")
                    
            except Exception as e:
                print(f"Error in background fetch loop page {p}: {e}")
                break
    
    # CLEANUP STALE JOBS - DISABLED for performance
    # Aggressive cleanup on every search was causing slowdowns with 90+ DB writes per search
    # Jobs naturally age out via the 1-hour Redis cache and can be manually invalidated if needed
    # TODO: Implement lazy cleanup - only mark jobs inactive if not seen in 7+ days
