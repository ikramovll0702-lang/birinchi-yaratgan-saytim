from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from app.templates_helper import render
from app.auth import get_current_user, require_roles, log_activity
from app.database import get_db
from app.services.academic_service import (
    get_all_faculties, get_all_departments, get_all_specialties, get_all_groups
)

router = APIRouter(prefix="/faculties", tags=["faculties"])

@router.get("", response_class=HTMLResponse)
async def list_faculties(request: Request, current_user: dict = Depends(get_current_user)):
    faculties = get_all_faculties()
    departments = get_all_departments()
    specialties = get_all_specialties()
    return render(request, "faculties/list.html", {
        "current_user": current_user,
        "faculties": faculties,
        "departments": departments,
        "specialties": specialties
    })

@router.post("/new")
async def create_faculty(
    code: str = Form(...),
    name: str = Form(...),
    dean_name: str = Form(""),
    phone: str = Form(""),
    description: str = Form(""),
    current_user: dict = Depends(require_roles("admin"))
):
    with get_db() as conn:
        conn.execute("""
            INSERT INTO faculties (code, name, dean_name, phone, description)
            VALUES (?, ?, ?, ?, ?)
        """, (code.strip().upper(), name.strip(), dean_name.strip(), phone.strip(), description.strip()))
    log_activity(current_user["id"], current_user["full_name"], "FACULTY_CREATE", f"Yangi fakultet qo'shildi: {name}")
    return RedirectResponse(url="/faculties", status_code=status.HTTP_302_FOUND)

@router.get("/groups", response_class=HTMLResponse)
async def list_groups(request: Request, current_user: dict = Depends(get_current_user)):
    groups = get_all_groups()
    faculties = get_all_faculties()
    specialties = get_all_specialties()
    return render(request, "faculties/groups.html", {
        "current_user": current_user,
        "groups": groups,
        "faculties": faculties,
        "specialties": specialties
    })

@router.post("/groups/new")
async def create_group(
    name: str = Form(...),
    faculty_id: int = Form(...),
    specialty_id: int = Form(...),
    course_level: int = Form(1),
    education_type: str = Form("Kunduzgi"),
    language: str = Form("O'zbek"),
    tutor_name: str = Form(""),
    current_user: dict = Depends(require_roles("admin", "dean"))
):
    with get_db() as conn:
        conn.execute("""
            INSERT INTO groups (name, faculty_id, specialty_id, course_level, education_type, language, tutor_name)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name.strip(), faculty_id, specialty_id, course_level, education_type, language, tutor_name.strip()))
    log_activity(current_user["id"], current_user["full_name"], "GROUP_CREATE", f"Yangi guruh ochildi: {name}")
    return RedirectResponse(url="/faculties/groups", status_code=status.HTTP_302_FOUND)
