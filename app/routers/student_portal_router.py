from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from typing import Optional
from app.templates_helper import render
from app.auth import get_current_user
from app.services.student_service import get_student_by_id
from app.services.grade_service import get_student_transcript
from app.services.attendance_service import get_student_attendance_history
from app.services.academic_service import get_timetable_for_group

router = APIRouter(prefix="/portal", tags=["portal"])

@router.get("", response_class=HTMLResponse)
async def student_portal(
    request: Request,
    student_id: Optional[int] = None,
    current_user: dict = Depends(get_current_user)
):
    target_student_id = current_user.get("student_id")
    if not target_student_id or current_user["role"] in ["admin", "dean", "teacher"]:
        target_student_id = student_id or 1

    student = get_student_by_id(target_student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Talaba topilmadi")

    transcript = get_student_transcript(target_student_id)
    attendance_history = get_student_attendance_history(target_student_id)
    timetable = get_timetable_for_group(student["group_id"])

    return render(request, "student_portal/dashboard.html", {
        "current_user": current_user,
        "student": student,
        "transcript": transcript,
        "attendance_history": attendance_history,
        "timetable": timetable
    })
