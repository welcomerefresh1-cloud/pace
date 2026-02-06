from fastapi import FastAPI
from routers import users, degrees, student_records, alumni, auth

app = FastAPI(
    title="Pasig Alumni and Career Employment (PACE) System",
    version="1.0.0"
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(degrees.router)
app.include_router(student_records.router)
app.include_router(alumni.router)


@app.get("/")
def read_root():
    return {"message": "Hello from PACE Backend"}
