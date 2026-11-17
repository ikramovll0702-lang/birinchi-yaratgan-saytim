from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Optional
from app.templates_helper import render
from app.auth import get_current_user, require_roles, log_activity
from app.database import get_db
from app.models import GradeInput
from app.services.academic_service import get_all_groups, get_all_subjects
from app.services.grade_service import save_or_update_grade

router = APIRouter(prefix="/grades", tags=["grades"])

@router.get("", response_class=HTMLResponse)
async def grades_journal_page(
    request: Request,
    group_id: Optional[int] = None,
    subject_id: Optional[int] = None,
    current_user: dict = Depends(get_current_user)
):
    groups = get_all_groups()
    subjects = get_all_subjects()

    selected_group = None
    selected_subject = None
    student_grades = []

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
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    s.id as student_id, s.full_name, s.student_code,
                    g.current_grade, g.midterm_grade, g.final_grade,
                    g.total_score, g.letter_grade, g.gpa_point, g.status
                FROM students s
                LEFT JOIN grades g ON g.student_id = s.id AND g.subject_id = ?
                WHERE s.group_id = ? AND s.status = 'O''qimoqda'
                ORDER BY s.full_name ASC
            """, (selected_subject["id"], selected_group["id"]))
            student_grades = [dict(r) for r in cursor.fetchall()]

    return render(request, "grades/journal.html", {
        "current_user": current_user,
        "groups": groups,
        "subjects": subjects,
        "selected_group": selected_group,
        "selected_subject": selected_subject,
        "student_grades": student_grades
    })

@router.post("/save")
async def save_grade_api(
    data: GradeInput,
    current_user: dict = Depends(require_roles("admin", "dean", "teacher"))
):
    result = save_or_update_grade(
        student_id=data.student_id,
        subject_id=data.subject_id,
        semester=data.semester,
        academic_year=data.academic_year,
        current_grade=data.current_grade,
        midterm_grade=data.midterm_grade,
        final_grade=data.final_grade
    )
    log_activity(current_user["id"], current_user["full_name"], "GRADE_UPDATE", f"Baho kiritildi: Student={data.student_id}, Subject={data.subject_id}, Total={result['total_score']}")
    return JSONResponse(content={"success": True, "result": result})
