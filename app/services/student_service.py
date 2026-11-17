from typing import List, Dict, Any, Optional, Tuple
import datetime
from app.database import get_db
from app.services.grade_service import calculate_student_gpa
from app.auth import hash_password

def get_students(
    search: Optional[str] = None,
    faculty_id: Optional[int] = None,
    specialty_id: Optional[int] = None,
    group_id: Optional[int] = None,
    course_level: Optional[int] = None,
    payment_form: Optional[str] = None,
    status: Optional[str] = None,
    gender: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
) -> Tuple[List[Dict[str, Any]], int]:
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            SELECT 
                s.id, s.student_code, s.full_name, s.first_name, s.last_name, s.middle_name,
                s.pinfl, s.passport_number, s.birth_date, s.gender, s.phone, s.email,
                s.payment_form, s.education_type, s.education_degree, s.course_level,
                s.admission_year, s.status, s.photo_url,
                g.id as group_id, g.name as group_name,
                f.id as faculty_id, f.name as faculty_name,
                sp.id as specialty_id, sp.name as specialty_name, sp.code as specialty_code
            FROM students s
            JOIN groups g ON s.group_id = g.id
            JOIN faculties f ON s.faculty_id = f.id
            JOIN specialties sp ON s.specialty_id = sp.id
            WHERE 1=1
        """
        count_query = """
            SELECT COUNT(*)
            FROM students s
            JOIN groups g ON s.group_id = g.id
            JOIN faculties f ON s.faculty_id = f.id
            JOIN specialties sp ON s.specialty_id = sp.id
            WHERE 1=1
        """
        params = []
        count_params = []

        if search:
            search_clause = " AND (s.full_name LIKE ? OR s.student_code LIKE ? OR s.pinfl LIKE ? OR s.passport_number LIKE ?)"
            val = f"%{search.strip()}%"
            query += search_clause
            count_query += search_clause
            params.extend([val, val, val, val])
            count_params.extend([val, val, val, val])

        if faculty_id:
            query += " AND s.faculty_id = ?"
            count_query += " AND s.faculty_id = ?"
            params.append(faculty_id)
            count_params.append(faculty_id)

        if specialty_id:
            query += " AND s.specialty_id = ?"
            count_query += " AND s.specialty_id = ?"
            params.append(specialty_id)
            count_params.append(specialty_id)

        if group_id:
            query += " AND s.group_id = ?"
            count_query += " AND s.group_id = ?"
            params.append(group_id)
            count_params.append(group_id)

        if course_level:
            query += " AND s.course_level = ?"
            count_query += " AND s.course_level = ?"
            params.append(course_level)
            count_params.append(course_level)

        if payment_form:
            query += " AND s.payment_form = ?"
            count_query += " AND s.payment_form = ?"
            params.append(payment_form)
            count_params.append(payment_form)

        if status:
            query += " AND s.status = ?"
            count_query += " AND s.status = ?"
            params.append(status)
            count_params.append(status)

        if gender:
            query += " AND s.gender = ?"
            count_query += " AND s.gender = ?"
            params.append(gender)
            count_params.append(gender)

        cursor.execute(count_query, count_params)
        total_count = cursor.fetchone()[0]

        query += " ORDER BY s.id DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        cursor.execute(query, params)
        students = [dict(row) for row in cursor.fetchall()]

        # Attach GPA
        for st in students:
            st["gpa"] = calculate_student_gpa(st["id"])

        return students, total_count

def get_student_by_id(student_id: int) -> Optional[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                s.*,
                g.name as group_name, g.academic_year as group_academic_year, g.language as group_language, g.tutor_name,
                f.name as faculty_name, f.code as faculty_code, f.dean_name,
                sp.name as specialty_name, sp.code as specialty_code, sp.degree as specialty_degree
            FROM students s
            JOIN groups g ON s.group_id = g.id
            JOIN faculties f ON s.faculty_id = f.id
            JOIN specialties sp ON s.specialty_id = sp.id
            WHERE s.id = ?
        """, (student_id,))
        row = cursor.fetchone()
        if not row:
            return None
        student = dict(row)
        student["gpa"] = calculate_student_gpa(student_id)

        # Get Contract status
        cursor.execute("SELECT * FROM contracts WHERE student_id = ? ORDER BY id DESC LIMIT 1", (student_id,))
        contract_row = cursor.fetchone()
        student["contract"] = dict(contract_row) if contract_row else None

        # Get Dormitory status
        cursor.execute("""
            SELECT dr.*, r.building, r.room_number, r.floor
            FROM dormitory_residents dr
            JOIN dormitory_rooms r ON dr.room_id = r.id
            WHERE dr.student_id = ? AND dr.status = 'Yashamoqda'
            LIMIT 1
        """, (student_id,))
        dorm_row = cursor.fetchone()
        student["dormitory"] = dict(dorm_row) if dorm_row else None

        # Get missed attendance hours
        cursor.execute("""
            SELECT 
                SUM(CASE WHEN status = 'Sababsiz' THEN hours ELSE 0 END) as unexcused_hours,
                SUM(CASE WHEN status = 'Sababli' THEN hours ELSE 0 END) as excused_hours,
                SUM(hours) as total_missed_hours
            FROM attendance
            WHERE student_id = ?
        """, (student_id,))
        att_row = cursor.fetchone()
        student["attendance_summary"] = dict(att_row) if att_row else {"unexcused_hours": 0, "excused_hours": 0, "total_missed_hours": 0}

        return student

def generate_next_student_code() -> str:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT student_code FROM students ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        current_year = datetime.datetime.now().year % 100
        prefix = f"395{current_year}"
        if row and row["student_code"] and str(row["student_code"]).startswith(prefix):
            try:
                num = int(row["student_code"][len(prefix):]) + 1
                return f"{prefix}{num:05d}"
            except ValueError:
                pass
        return f"{prefix}10001"

def create_student(data: Dict[str, Any]) -> int:
    first_name = data["first_name"].strip()
    last_name = data["last_name"].strip()
    middle_name = (data.get("middle_name") or "").strip()
    full_name = f"{last_name} {first_name} {middle_name}".strip()
    
    student_code = data.get("student_code")
    if not student_code:
        student_code = generate_next_student_code()
    else:
        student_code = str(student_code).strip()

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO students (
                student_code, first_name, last_name, middle_name, full_name,
                pinfl, passport_number, birth_date, gender, nationality,
                phone, email, address, region, district, parent_phone,
                group_id, faculty_id, specialty_id, payment_form,
                education_type, education_degree, course_level, admission_year,
                status, photo_url, notes
            ) VALUES (
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?,
                ?, ?, ?, ?,
                ?, ?, ?
            )
        """, (
            student_code, first_name, last_name, middle_name, full_name,
            data.get("pinfl", ""), data.get("passport_number", ""), data.get("birth_date", ""),
            data.get("gender", "Erkak"), data.get("nationality", "O'zbek"),
            data.get("phone", ""), data.get("email", ""), data.get("address", ""),
            data.get("region", ""), data.get("district", ""), data.get("parent_phone", ""),
            data["group_id"], data["faculty_id"], data["specialty_id"],
            data.get("payment_form", "To'lov-shartnoma"), data.get("education_type", "Kunduzgi"),
            data.get("education_degree", "Bakalavr"), data.get("course_level", 1),
            data.get("admission_year", datetime.datetime.now().year),
            data.get("status", "O'qimoqda"), data.get("photo_url", ""), data.get("notes", "")
        ))
        student_id = cursor.lastrowid

        # Auto-create user account for student portal
        username = student_code.lower()
        password_raw = "student123" # default password
        hashed_pwd = hash_password(password_raw)
        
        cursor.execute("""
            INSERT OR IGNORE INTO users (username, password_hash, full_name, role, email, phone, student_id)
            VALUES (?, ?, ?, 'student', ?, ?, ?)
        """, (username, hashed_pwd, full_name, data.get("email", ""), data.get("phone", ""), student_id))

        # If payment_form is To'lov-shartnoma, create contract record
        if data.get("payment_form") == "To'lov-shartnoma":
            contract_num = f"SH-{student_code[-5:]}/2025"
            total_sum = 12000000.0 # Standard base contract in UZS
            cursor.execute("""
                INSERT OR IGNORE INTO contracts (student_id, academic_year, contract_number, total_amount, paid_amount, status)
                VALUES (?, '2025-2026', ?, ?, 0, 'Qarzdor')
            """, (student_id, contract_num, total_sum))

        return student_id

def update_student(student_id: int, data: Dict[str, Any]) -> bool:
    first_name = data["first_name"].strip()
    last_name = data["last_name"].strip()
    middle_name = (data.get("middle_name") or "").strip()
    full_name = f"{last_name} {first_name} {middle_name}".strip()

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE students SET
                first_name = ?, last_name = ?, middle_name = ?, full_name = ?,
                pinfl = ?, passport_number = ?, birth_date = ?, gender = ?, nationality = ?,
                phone = ?, email = ?, address = ?, region = ?, district = ?, parent_phone = ?,
                group_id = ?, faculty_id = ?, specialty_id = ?, payment_form = ?,
                education_type = ?, education_degree = ?, course_level = ?, admission_year = ?,
                status = ?, notes = ?
            WHERE id = ?
        """, (
            first_name, last_name, middle_name, full_name,
            data.get("pinfl", ""), data.get("passport_number", ""), data.get("birth_date", ""),
            data.get("gender", "Erkak"), data.get("nationality", "O'zbek"),
            data.get("phone", ""), data.get("email", ""), data.get("address", ""),
            data.get("region", ""), data.get("district", ""), data.get("parent_phone", ""),
            data["group_id"], data["faculty_id"], data["specialty_id"],
            data.get("payment_form", "To'lov-shartnoma"), data.get("education_type", "Kunduzgi"),
            data.get("education_degree", "Bakalavr"), data.get("course_level", 1),
            data.get("admission_year", 2024), data.get("status", "O'qimoqda"),
            data.get("notes", ""), student_id
        ))
        
        cursor.execute("UPDATE users SET full_name = ? WHERE student_id = ?", (full_name, student_id))
        return cursor.rowcount > 0

def delete_student(student_id: int) -> bool:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE student_id = ?", (student_id,))
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        return cursor.rowcount > 0
