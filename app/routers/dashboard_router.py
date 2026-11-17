from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
import datetime
from app.templates_helper import render
from app.database import get_db
from app.auth import get_current_user
from app.services.student_service import get_students
from app.services.attendance_service import get_attendance_warnings
from app.services.finance_service import get_finance_overview

router = APIRouter(tags=["dashboard"])

@router.get("/", response_class=HTMLResponse)
@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_index(request: Request, current_user: dict = Depends(get_current_user)):
    if current_user["role"] == "student":
        return RedirectResponse(url="/portal")

    with get_db() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM students")
        total_students = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM students WHERE status = 'O''qimoqda'")
        active_students = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM faculties")
        faculties_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM groups")
        groups_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM specialties")
        specialties_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM students WHERE payment_form = 'Davlat granti'")
        grant_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM students WHERE payment_form = 'To''lov-shartnoma'")
        contract_count = cursor.fetchone()[0]

        cursor.execute("""
            SELECT AVG(g.gpa_point)
            FROM grades g
            JOIN students s ON g.student_id = s.id
            WHERE s.status = 'O''qimoqda' AND g.total_score > 0
        """)
        avg_row = cursor.fetchone()[0]
        average_gpa = round(avg_row, 2) if avg_row else 3.45

        cursor.execute("""
            SELECT f.code, f.name, COUNT(s.id) as st_count
            FROM faculties f
            LEFT JOIN students s ON s.faculty_id = f.id
            GROUP BY f.id
            ORDER BY f.id ASC
        """)
        fac_rows = cursor.fetchall()
        faculty_chart_labels = [r["code"] for r in fac_rows]
        faculty_chart_data = [r["st_count"] for r in fac_rows]

        course_counts = [0, 0, 0, 0]
        cursor.execute("""
            SELECT course_level, COUNT(*) as cnt
            FROM students
            WHERE status = 'O''qimoqda'
            GROUP BY course_level
        """)
        for r in cursor.fetchall():
            lvl = r["course_level"]
            if 1 <= lvl <= 4:
                course_counts[lvl - 1] = r["cnt"]

    warnings = get_attendance_warnings(74)
    warning_students_count = len(warnings)

    finance = get_finance_overview()
    recent_students, _ = get_students(limit=5)
    current_date = datetime.datetime.now().strftime("%d-%B, %Y-yil")

    return render(request, "dashboard/index.html", {
        "current_user": current_user,
        "current_date": current_date,
        "stats": {
            "total_students": total_students,
            "active_students": active_students,
            "faculties_count": faculties_count,
            "groups_count": groups_count,
            "specialties_count": specialties_count,
            "average_gpa": average_gpa,
            "warning_students_count": warning_students_count,
            "grant_count": grant_count,
            "contract_count": contract_count,
        },
        "finance": finance,
        "faculty_chart_labels": faculty_chart_labels,
        "faculty_chart_data": faculty_chart_data,
        "course_chart_data": course_counts,
        "recent_students": recent_students,
    })
