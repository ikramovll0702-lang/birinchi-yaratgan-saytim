from fastapi import APIRouter, Request, Depends, Form, UploadFile, File, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from typing import Optional
from app.templates_helper import render
from app.auth import get_current_user, require_roles, log_activity
from app.services.student_service import (
    get_students, get_student_by_id, create_student, update_student, delete_student
)
from app.services.academic_service import (
    get_all_faculties, get_all_specialties, get_all_groups
)
from app.services.grade_service import get_student_transcript
from app.services.attendance_service import get_student_attendance_history
from app.services.pdf_service import (
    generate_student_certificate_pdf, generate_transcript_pdf, generate_student_id_card_pdf
)
from app.services.excel_service import (
    export_students_to_excel, generate_sample_import_template, import_students_from_excel
)

router = APIRouter(prefix="/students", tags=["students"])

@router.get("", response_class=HTMLResponse)
async def list_students(
    request: Request,
    search: Optional[str] = None,
    faculty_id: Optional[int] = None,
    specialty_id: Optional[int] = None,
    group_id: Optional[int] = None,
    course_level: Optional[int] = None,
    payment_form: Optional[str] = None,
    status: Optional[str] = None,
    gender: Optional[str] = None,
    page: int = 1,
    current_user: dict = Depends(get_current_user)
):
    limit = 50
    offset = (page - 1) * limit
    students, total_count = get_students(
        search=search,
        faculty_id=faculty_id,
        specialty_id=specialty_id,
        group_id=group_id,
        course_level=course_level,
        payment_form=payment_form,
        status=status,
        gender=gender,
        limit=limit,
        offset=offset
    )

    faculties = get_all_faculties()
    specialties = get_all_specialties()
    groups = get_all_groups()

    return render(request, "students/list.html", {
        "current_user": current_user,
        "students": students,
        "total_count": total_count,
        "faculties": faculties,
        "specialties": specialties,
        "groups": groups,
        "search": search,
        "faculty_id": faculty_id,
        "specialty_id": specialty_id,
        "group_id": group_id,
        "course_level": course_level,
        "payment_form": payment_form,
        "status": status,
        "gender": gender
    })

@router.get("/new", response_class=HTMLResponse)
async def new_student_page(request: Request, current_user: dict = Depends(require_roles("admin", "dean"))):
    faculties = get_all_faculties()
    specialties = get_all_specialties()
    groups = get_all_groups()
    return render(request, "students/form.html", {
        "current_user": current_user,
        "student": None,
        "faculties": faculties,
        "specialties": specialties,
        "groups": groups,
        "error": None
    })

@router.post("/new", response_class=HTMLResponse)
async def new_student_submit(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    middle_name: Optional[str] = Form(""),
    pinfl: Optional[str] = Form(""),
    passport_number: Optional[str] = Form(""),
    birth_date: Optional[str] = Form(""),
    gender: str = Form("Erkak"),
    phone: Optional[str] = Form(""),
    email: Optional[str] = Form(""),
    parent_phone: Optional[str] = Form(""),
    region: Optional[str] = Form(""),
    district: Optional[str] = Form(""),
    address: Optional[str] = Form(""),
    faculty_id: int = Form(...),
    specialty_id: int = Form(...),
    group_id: int = Form(...),
    course_level: int = Form(1),
    education_degree: str = Form("Bakalavr"),
    education_type: str = Form("Kunduzgi"),
    payment_form: str = Form("To'lov-shartnoma"),
    status: str = Form("O'qimoqda"),
    admission_year: int = Form(2024),
    current_user: dict = Depends(require_roles("admin", "dean"))
):
    data = {
        "first_name": first_name,
        "last_name": last_name,
        "middle_name": middle_name,
        "pinfl": pinfl,
        "passport_number": passport_number,
        "birth_date": birth_date,
        "gender": gender,
        "phone": phone,
        "email": email,
        "parent_phone": parent_phone,
        "region": region,
        "district": district,
        "address": address,
        "faculty_id": faculty_id,
        "specialty_id": specialty_id,
        "group_id": group_id,
        "course_level": course_level,
        "education_degree": education_degree,
        "education_type": education_type,
        "payment_form": payment_form,
        "status": status,
        "admission_year": admission_year
    }
    try:
        student_id = create_student(data)
        log_activity(current_user["id"], current_user["full_name"], "STUDENT_CREATE", f"Yangi talaba qo'shildi: {last_name} {first_name}")
        return RedirectResponse(url=f"/students/{student_id}", status_code=status.HTTP_302_FOUND)
    except Exception as e:
        faculties = get_all_faculties()
        specialties = get_all_specialties()
        groups = get_all_groups()
        return render(request, "students/form.html", {
            "current_user": current_user,
            "student": data,
            "faculties": faculties,
            "specialties": specialties,
            "groups": groups,
            "error": f"Talabani saqlashda xatolik: {str(e)}"
        })

@router.get("/export/excel")
async def export_excel(
    request: Request,
    search: Optional[str] = None,
    faculty_id: Optional[int] = None,
    specialty_id: Optional[int] = None,
    group_id: Optional[int] = None,
    course_level: Optional[int] = None,
    payment_form: Optional[str] = None,
    status: Optional[str] = None,
    gender: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    students, _ = get_students(
        search=search,
        faculty_id=faculty_id,
        specialty_id=specialty_id,
        group_id=group_id,
        course_level=course_level,
        payment_form=payment_form,
        status=status,
        gender=gender,
        limit=5000
    )
    buffer = export_students_to_excel(students)
    log_activity(current_user["id"], current_user["full_name"], "EXCEL_EXPORT", "Talabalar ro'yxati Excelga eksport qilindi")
    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=talabalar_royxati.xlsx"}
    )

@router.get("/import/sample-template")
async def sample_template():
    buffer = generate_sample_import_template()
    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=talaba_import_shablon.xlsx"}
    )

@router.get("/import/excel", response_class=HTMLResponse)
async def import_page(request: Request, current_user: dict = Depends(require_roles("admin", "dean"))):
    return render(request, "students/import.html", {
        "current_user": current_user,
        "message": None,
        "errors": None
    })

@router.post("/import/excel", response_class=HTMLResponse)
async def import_excel(
    request: Request,
    file: UploadFile = File(...),
    current_user: dict = Depends(require_roles("admin", "dean"))
):
    contents = await file.read()
    res = import_students_from_excel(contents)
    log_activity(current_user["id"], current_user["full_name"], "EXCEL_IMPORT", f"{res['count']} ta talaba import qilindi")
    return render(request, "students/import.html", {
        "current_user": current_user,
        "message": f"Muvaffaqiyatli import qilindi: {res['count']} ta talaba bazaga qo'shildi!" if res["count"] > 0 else None,
        "errors": res["errors"]
    })

@router.get("/{student_id}", response_class=HTMLResponse)
async def view_student(student_id: int, request: Request, current_user: dict = Depends(get_current_user)):
    student = get_student_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Talaba topilmadi")

    transcript = get_student_transcript(student_id)
    attendance_history = get_student_attendance_history(student_id)

    return render(request, "students/detail.html", {
        "current_user": current_user,
        "student": student,
        "transcript": transcript,
        "attendance_history": attendance_history
    })

@router.get("/{student_id}/edit", response_class=HTMLResponse)
async def edit_student_page(student_id: int, request: Request, current_user: dict = Depends(require_roles("admin", "dean"))):
    student = get_student_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Talaba topilmadi")
    faculties = get_all_faculties()
    specialties = get_all_specialties()
    groups = get_all_groups()
    return render(request, "students/form.html", {
        "current_user": current_user,
        "student": student,
        "faculties": faculties,
        "specialties": specialties,
        "groups": groups,
        "error": None
    })

@router.post("/{student_id}/edit", response_class=HTMLResponse)
async def edit_student_submit(
    student_id: int,
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    middle_name: Optional[str] = Form(""),
    pinfl: Optional[str] = Form(""),
    passport_number: Optional[str] = Form(""),
    birth_date: Optional[str] = Form(""),
    gender: str = Form("Erkak"),
    phone: Optional[str] = Form(""),
    email: Optional[str] = Form(""),
    parent_phone: Optional[str] = Form(""),
    region: Optional[str] = Form(""),
    district: Optional[str] = Form(""),
    address: Optional[str] = Form(""),
    faculty_id: int = Form(...),
    specialty_id: int = Form(...),
    group_id: int = Form(...),
    course_level: int = Form(1),
    education_degree: str = Form("Bakalavr"),
    education_type: str = Form("Kunduzgi"),
    payment_form: str = Form("To'lov-shartnoma"),
    status: str = Form("O'qimoqda"),
    admission_year: int = Form(2024),
    current_user: dict = Depends(require_roles("admin", "dean"))
):
    data = {
        "first_name": first_name,
        "last_name": last_name,
        "middle_name": middle_name,
        "pinfl": pinfl,
        "passport_number": passport_number,
        "birth_date": birth_date,
        "gender": gender,
        "phone": phone,
        "email": email,
        "parent_phone": parent_phone,
        "region": region,
        "district": district,
        "address": address,
        "faculty_id": faculty_id,
        "specialty_id": specialty_id,
        "group_id": group_id,
        "course_level": course_level,
        "education_degree": education_degree,
        "education_type": education_type,
        "payment_form": payment_form,
        "status": status,
        "admission_year": admission_year
    }
    update_student(student_id, data)
    log_activity(current_user["id"], current_user["full_name"], "STUDENT_UPDATE", f"Talaba ma'lumotlari yangilandi ID={student_id}")
    return RedirectResponse(url=f"/students/{student_id}", status_code=status.HTTP_302_FOUND)

@router.post("/{student_id}/delete")
async def delete_student_action(student_id: int, current_user: dict = Depends(require_roles("admin"))):
    delete_student(student_id)
    log_activity(current_user["id"], current_user["full_name"], "STUDENT_DELETE", f"Talaba o'chirildi ID={student_id}")
    return RedirectResponse(url="/students", status_code=status.HTTP_302_FOUND)

@router.get("/{student_id}/certificate.pdf")
async def download_certificate(student_id: int, current_user: dict = Depends(get_current_user)):
    student = get_student_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Talaba topilmadi")
    buffer = generate_student_certificate_pdf(student)
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename=malumotnoma_{student['student_code']}.pdf"}
    )

@router.get("/{student_id}/transcript.pdf")
async def download_transcript(student_id: int, current_user: dict = Depends(get_current_user)):
    student = get_student_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Talaba topilmadi")
    buffer = generate_transcript_pdf(student)
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename=transkript_{student['student_code']}.pdf"}
    )

@router.get("/{student_id}/id-card.pdf")
async def download_id_card(student_id: int, current_user: dict = Depends(get_current_user)):
    student = get_student_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Talaba topilmadi")
    buffer = generate_student_id_card_pdf(student)
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename=id_card_{student['student_code']}.pdf"}
    )
