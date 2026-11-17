from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Optional
from app.templates_helper import render
from app.auth import get_current_user, require_roles, log_activity
from app.database import get_db
from app.services.academic_service import (
    get_all_subjects, get_all_teachers, get_all_departments, get_all_groups, get_group_by_id, get_timetable_for_group
)

router = APIRouter(prefix="/academics", tags=["academics"])

@router.get("/subjects", response_class=HTMLResponse)
async def subjects_page(request: Request, current_user: dict = Depends(get_current_user)):
    subjects = get_all_subjects()
    teachers = get_all_teachers()
    departments = get_all_departments()
    return render(request, "academics/subjects.html", {
        "current_user": current_user,
        "subjects": subjects,
        "teachers": teachers,
        "departments": departments
    })

@router.post("/subjects/new")
async def create_subject_submit(
    code: str = Form(...),
    name: str = Form(...),
    department_id: int = Form(...),
    credits: int = Form(4),
    semester: int = Form(1),
    lecture_hours: int = Form(30),
    practice_hours: int = Form(30),
    lab_hours: int = Form(0),
    independent_hours: int = Form(60),
    current_user: dict = Depends(require_roles("admin", "dean"))
):
    total = lecture_hours + practice_hours + lab_hours + independent_hours
    with get_db() as conn:
        conn.execute("""
            INSERT INTO subjects (code, name, department_id, credits, total_hours, lecture_hours, practice_hours, lab_hours, independent_hours, semester)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (code.strip().upper(), name.strip(), department_id, credits, total, lecture_hours, practice_hours, lab_hours, independent_hours, semester))
    log_activity(current_user["id"], current_user["full_name"], "SUBJECT_CREATE", f"Yangi fan qo'shildi: {name}")
    return RedirectResponse(url="/academics/subjects", status_code=status.HTTP_302_FOUND)

@router.get("/timetable", response_class=HTMLResponse)
async def timetable_page(request: Request, group_id: Optional[int] = None, current_user: dict = Depends(get_current_user)):
    groups = get_all_groups()
    selected_group = None
    timetable = []
    
    if groups:
        if group_id:
            selected_group = get_group_by_id(group_id)
        else:
            selected_group = groups[0]
            group_id = selected_group["id"]

        if selected_group:
            timetable = get_timetable_for_group(selected_group["id"])

    return render(request, "academics/timetable.html", {
        "current_user": current_user,
        "groups": groups,
        "selected_group": selected_group,
        "timetable": timetable
    })
