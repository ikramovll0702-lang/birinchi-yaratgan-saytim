import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.database import init_db
from app.seed_data_auto import ensure_initial_seed
from app.templates_helper import render
from app.routers.auth_router import router as auth_router
from app.routers.dashboard_router import router as dashboard_router
from app.routers.students_router import router as students_router
from app.routers.faculties_router import router as faculties_router
from app.routers.academics_router import router as academics_router
from app.routers.grades_router import router as grades_router
from app.routers.attendance_router import router as attendance_router
from app.routers.finance_router import router as finance_router
from app.routers.dormitory_router import router as dormitory_router
from app.routers.student_portal_router import router as student_portal_router
from app.routers.api_router import router as api_router

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB schema
    init_db()
    # Automatically seed initial demo data if database is clean
    ensure_initial_seed()
    yield

app = FastAPI(
    title="HEMIS - Oliy Ta'lim Muassasasi Talabalar Boshqaruv Tizimi",
    description="Student Information Management System (HEMIS) for Higher Education Institutions",
    version="2.5.0",
    lifespan=lifespan
)

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Include all routers
app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(students_router)
app.include_router(faculties_router)
app.include_router(academics_router)
app.include_router(grades_router)
app.include_router(attendance_router)
app.include_router(finance_router)
app.include_router(dormitory_router)
app.include_router(student_portal_router)
app.include_router(api_router)

# PWA Manifest and Service Worker
@app.get("/manifest.json", include_in_schema=False)
async def get_manifest():
    return FileResponse(os.path.join(STATIC_DIR, "manifest.json"), media_type="application/manifest+json")

@app.get("/sw.js", include_in_schema=False)
async def get_sw():
    return FileResponse(
        os.path.join(STATIC_DIR, "sw.js"),
        media_type="application/javascript",
        headers={"Service-Worker-Allowed": "/"}
    )

# Custom 404 handler
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return render(request, "base.html", {
        "current_user": None,
        "title": "Sahifa topilmadi - 404"
    }, status_code=404)

# Custom 403 handler
@app.exception_handler(403)
async def forbidden_handler(request: Request, exc):
    return render(request, "base.html", {
        "current_user": None,
        "title": "Ruxsat etilmagan - 403"
    }, status_code=403)
