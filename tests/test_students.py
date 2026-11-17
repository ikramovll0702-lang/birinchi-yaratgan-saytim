import pytest
from app.services.student_service import (
    get_students, get_student_by_id, create_student, update_student, delete_student, generate_next_student_code
)

def test_get_students():
    students, total = get_students(limit=10)
    assert total > 0
    assert len(students) > 0
    first = students[0]
    assert "student_code" in first
    assert "full_name" in first
    assert "gpa" in first

def test_get_student_by_id():
    student = get_student_by_id(1)
    assert student is not None
    assert student["id"] == 1
    assert "faculty_name" in student
    assert "group_name" in student
    assert "gpa" in student
    assert "attendance_summary" in student

def test_student_code_generation():
    code = generate_next_student_code()
    assert code is not None
    assert len(code) >= 10

def test_create_and_delete_student():
    data = {
        "first_name": "Testbek",
        "last_name": "Sinovov",
        "middle_name": "Sinov o'g'li",
        "pinfl": "99999999999999",
        "passport_number": "TT9999999",
        "birth_date": "2004-05-10",
        "gender": "Erkak",
        "group_id": 1,
        "faculty_id": 1,
        "specialty_id": 1,
        "payment_form": "To'lov-shartnoma",
        "education_type": "Kunduzgi",
        "education_degree": "Bakalavr",
        "course_level": 1,
        "status": "O'qimoqda"
    }
    st_id = create_student(data)
    assert st_id is not None
    assert st_id > 0

    created = get_student_by_id(st_id)
    assert created is not None
    assert created["first_name"] == "Testbek"

    # Update
    data["first_name"] = "Yangilangan"
    updated = update_student(st_id, data)
    assert updated is True
    assert get_student_by_id(st_id)["first_name"] == "Yangilangan"

    # Delete
    deleted = delete_student(st_id)
    assert deleted is True
    assert get_student_by_id(st_id) is None

