from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

class UserLogin(BaseModel):
    username: str
    password: str

class StudentCreate(BaseModel):
    student_code: str
    first_name: str
    last_name: str
    middle_name: Optional[str] = ""
    pinfl: Optional[str] = ""
    passport_number: Optional[str] = ""
    birth_date: Optional[str] = ""
    gender: str = "Erkak"
    nationality: str = "O'zbek"
    phone: Optional[str] = ""
    email: Optional[str] = ""
    address: Optional[str] = ""
    region: Optional[str] = ""
    district: Optional[str] = ""
    parent_phone: Optional[str] = ""
    group_id: int
    faculty_id: int
    specialty_id: int
    payment_form: str = "To'lov-shartnoma"
    education_type: str = "Kunduzgi"
    education_degree: str = "Bakalavr"
    course_level: int = 1
    admission_year: int = 2024
    status: str = "O'qimoqda"
    notes: Optional[str] = ""

class StudentUpdate(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str] = ""
    pinfl: Optional[str] = ""
    passport_number: Optional[str] = ""
    birth_date: Optional[str] = ""
    gender: str = "Erkak"
    nationality: str = "O'zbek"
    phone: Optional[str] = ""
    email: Optional[str] = ""
    address: Optional[str] = ""
    region: Optional[str] = ""
    district: Optional[str] = ""
    parent_phone: Optional[str] = ""
    group_id: int
    faculty_id: int
    specialty_id: int
    payment_form: str
    education_type: str
    education_degree: str
    course_level: int
    admission_year: int
    status: str
    notes: Optional[str] = ""

class FacultyCreate(BaseModel):
    code: str
    name: str
    dean_name: Optional[str] = ""
    phone: Optional[str] = ""
    description: Optional[str] = ""

class DepartmentCreate(BaseModel):
    faculty_id: int
    name: str
    head_name: Optional[str] = ""
    phone: Optional[str] = ""

class SpecialtyCreate(BaseModel):
    faculty_id: int
    code: str
    name: str
    degree: str = "Bakalavriat"
    duration_years: int = 4

class GroupCreate(BaseModel):
    name: str
    faculty_id: int
    specialty_id: int
    course_level: int
    academic_year: str = "2025-2026"
    education_type: str = "Kunduzgi"
    language: str = "O'zbek"
    tutor_name: Optional[str] = ""

class SubjectCreate(BaseModel):
    code: str
    name: str
    department_id: int
    credits: int = 4
    total_hours: int = 120
    lecture_hours: int = 30
    practice_hours: int = 30
    lab_hours: int = 0
    independent_hours: int = 60
    semester: int = 1

class GradeInput(BaseModel):
    student_id: int
    subject_id: int
    semester: int
    academic_year: str = "2025-2026"
    current_grade: float = 0.0
    midterm_grade: float = 0.0
    final_grade: float = 0.0

class AttendanceInput(BaseModel):
    student_id: int
    subject_id: int
    group_id: int
    date: str
    pair_number: int
    status: str
    hours: int = 2
    notes: Optional[str] = ""

class ContractCreate(BaseModel):
    student_id: int
    academic_year: str = "2025-2026"
    contract_number: str
    total_amount: float
    paid_amount: float = 0
    due_date: Optional[str] = ""

class PaymentCreate(BaseModel):
    contract_id: int
    student_id: int
    amount: float
    payment_date: str
    payment_method: str = "Bank o'tkazmasi"
    receipt_number: Optional[str] = ""
    notes: Optional[str] = ""

