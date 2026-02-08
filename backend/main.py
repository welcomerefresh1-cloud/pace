# Trigger reload
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users, degrees, student_records, alumni, auth, jobs
from core.config import settings

app = FastAPI(
    title="Pasig Alumni and Career Employment (PACE) System",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(degrees.router)
app.include_router(student_records.router)
app.include_router(alumni.router)
app.include_router(jobs.router)


@app.get("/")
def read_root():
    return {"message": "Hello from PACE Backend v3"}


