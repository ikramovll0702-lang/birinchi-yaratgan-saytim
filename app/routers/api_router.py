from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from typing import Optional
from app.auth import get_current_user
from app.services.academic_service import get_all_specialties, get_all_groups
from app.services.student_service import get_students

router = APIRouter(prefix="/api", tags=["api"])

@router.get("/faculty/{faculty_id}/options")
async def faculty_options(faculty_id: int):
    specialties = get_all_specialties(faculty_id=faculty_id)
    groups = get_all_groups(faculty_id=faculty_id)
    return JSONResponse(content={
        "specialties": [{"id": s["id"], "name": s["name"], "code": s["code"]} for s in specialties],
        "groups": [{"id": g["id"], "name": g["name"], "course_level": g["course_level"]} for g in groups]
    })

@router.get("/students/search")
async def api_search_students(q: str = Query("", min_length=1)):
    students, count = get_students(search=q, limit=10)
    return JSONResponse(content={
        "total": count,
        "results": [
            {
                "id": s["id"],
                "student_code": s["student_code"],
                "full_name": s["full_name"],
                "group_name": s["group_name"],
                "faculty_name": s["faculty_name"]
            }
            for s in students
        ]
    })

