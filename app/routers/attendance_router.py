from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import HTMLResponse, JSONResponse
import datetime
from typing import Optional
from app.templates_helper import render
from app.auth import get_current_user, require_roles
from app.models import AttendanceInput
from app.services.academic_service import get_all_groups, get_all_subjects
from app.services.attendance_service import (
    mark_attendance, get_group_attendance_for_date, get_attendance_warnings
)

router = APIRouter(prefix="/attendance", tags=["attendance"])

@router.get("", response_class=HTMLResponse)
async def attendance_page(
    request: Request,
    group_id: Optional[int] = None,
    subject_id: Optional[int] = None,
    date: Optional[str] = None,
    pair_number: Optional[int] = 1,
    current_user: dict = Depends(get_current_user)
):
    groups = get_all_groups()
    subjects = get_all_subjects()

    selected_group = None
    selected_subject = None
    attendance_list = []

    if not date:
        date = datetime.datetime.now().strftime("%Y-%m-%d")

    if groups:
        if group_id:
            for g in groups:
                if g["id"] == group_id:
                    selected_group = g
                    break
        if not selected_group:
            selected_group = groups[0]

    if subjects:
        if subject_id:
            for s in subjects:
                if s["id"] == subject_id:
                    selected_subject = s
                    break
        if not selected_subject:
            selected_subject = subjects[0]

    if selected_group and selected_subject:
        attendance_list = get_group_attendance_for_date(
            group_id=selected_group["id"],
            subject_id=selected_subject["id"],
            date=date,
            pair_number=pair_number
        )

    return render(request, "attendance/mark.html", {
        "current_user": current_user,
        "groups": groups,
        "subjects": subjects,
        "selected_group": selected_group,
        "selected_subject": selected_subject,
        "selected_date": date,
        "selected_pair": pair_number,
        "attendance_list": attendance_list
    })

@router.post("/save")
async def save_attendance_api(
    data: AttendanceInput,
    current_user: dict = Depends(require_roles("admin", "dean", "teacher"))
):
    mark_attendance(
        student_id=data.student_id,
        subject_id=data.subject_id,
        group_id=data.group_id,
        date=data.date,
        pair_number=data.pair_number,
        status=data.status,
        hours=data.hours,
        notes=data.notes or ""
    )
    return JSONResponse(content={"success": True})

@router.get("/warnings", response_class=HTMLResponse)
async def attendance_warnings_page(request: Request, current_user: dict = Depends(get_current_user)):
    warnings = get_attendance_warnings(threshold_hours=74)
    return render(request, "attendance/warnings.html", {
        "current_user": current_user,
        "warnings": warnings
    })
