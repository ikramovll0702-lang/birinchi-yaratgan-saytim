from typing import List, Dict, Any, Optional
from app.database import get_db

def get_all_faculties() -> List[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT f.*, 
                   COUNT(DISTINCT sp.id) as specialties_count,
                   COUNT(DISTINCT g.id) as groups_count,
                   COUNT(DISTINCT s.id) as students_count
            FROM faculties f
            LEFT JOIN specialties sp ON sp.faculty_id = f.id
            LEFT JOIN groups g ON g.faculty_id = f.id
            LEFT JOIN students s ON s.faculty_id = f.id
            GROUP BY f.id
            ORDER BY f.name ASC
        """)
        return [dict(r) for r in cursor.fetchall()]

def get_faculty_by_id(faculty_id: int) -> Optional[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM faculties WHERE id = ?", (faculty_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def get_all_departments(faculty_id: Optional[int] = None) -> List[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            SELECT d.*, f.name as faculty_name,
                   COUNT(DISTINCT t.id) as teachers_count,
                   COUNT(DISTINCT sub.id) as subjects_count
            FROM departments d
            JOIN faculties f ON d.faculty_id = f.id
            LEFT JOIN teachers t ON t.department_id = d.id
            LEFT JOIN subjects sub ON sub.department_id = d.id
        """
        params = []
        if faculty_id:
            query += " WHERE d.faculty_id = ?"
            params.append(faculty_id)
        query += " GROUP BY d.id ORDER BY d.name ASC"
        cursor.execute(query, params)
        return [dict(r) for r in cursor.fetchall()]

def get_all_specialties(faculty_id: Optional[int] = None) -> List[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            SELECT sp.*, f.name as faculty_name,
                   COUNT(DISTINCT g.id) as groups_count,
                   COUNT(DISTINCT s.id) as students_count
            FROM specialties sp
            JOIN faculties f ON sp.faculty_id = f.id
            LEFT JOIN groups g ON g.specialty_id = sp.id
            LEFT JOIN students s ON s.specialty_id = sp.id
        """
        params = []
        if faculty_id:
            query += " WHERE sp.faculty_id = ?"
            params.append(faculty_id)
        query += " GROUP BY sp.id ORDER BY sp.name ASC"
        cursor.execute(query, params)
        return [dict(r) for r in cursor.fetchall()]

def get_all_groups(faculty_id: Optional[int] = None, course_level: Optional[int] = None) -> List[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            SELECT g.*, f.name as faculty_name, sp.name as specialty_name, sp.code as specialty_code,
                   COUNT(DISTINCT s.id) as students_count
            FROM groups g
            JOIN faculties f ON g.faculty_id = f.id
            JOIN specialties sp ON g.specialty_id = sp.id
            LEFT JOIN students s ON s.group_id = g.id
            WHERE 1=1
        """
        params = []
        if faculty_id:
            query += " AND g.faculty_id = ?"
            params.append(faculty_id)
        if course_level:
            query += " AND g.course_level = ?"
            params.append(course_level)
        query += " GROUP BY g.id ORDER BY g.course_level ASC, g.name ASC"
        cursor.execute(query, params)
        return [dict(r) for r in cursor.fetchall()]

def get_group_by_id(group_id: int) -> Optional[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT g.*, f.name as faculty_name, sp.name as specialty_name, sp.code as specialty_code
            FROM groups g
            JOIN faculties f ON g.faculty_id = f.id
            JOIN specialties sp ON g.specialty_id = sp.id
            WHERE g.id = ?
        """, (group_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def get_all_subjects(department_id: Optional[int] = None) -> List[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            SELECT s.*, d.name as department_name, f.name as faculty_name
            FROM subjects s
            JOIN departments d ON s.department_id = d.id
            JOIN faculties f ON d.faculty_id = f.id
        """
        params = []
        if department_id:
            query += " WHERE s.department_id = ?"
            params.append(department_id)
        query += " ORDER BY s.semester ASC, s.name ASC"
        cursor.execute(query, params)
        return [dict(r) for r in cursor.fetchall()]

def get_all_teachers(department_id: Optional[int] = None) -> List[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            SELECT t.*, d.name as department_name, f.name as faculty_name
            FROM teachers t
            JOIN departments d ON t.department_id = d.id
            JOIN faculties f ON d.faculty_id = f.id
        """
        params = []
        if department_id:
            query += " WHERE t.department_id = ?"
            params.append(department_id)
        query += " ORDER BY t.full_name ASC"
        cursor.execute(query, params)
        return [dict(r) for r in cursor.fetchall()]

def get_timetable_for_group(group_id: int) -> List[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT tt.*, s.name as subject_name, s.code as subject_code,
                   t.full_name as teacher_name
            FROM timetables tt
            JOIN subjects s ON tt.subject_id = s.id
            JOIN teachers t ON tt.teacher_id = t.id
            WHERE tt.group_id = ?
            ORDER BY tt.day_of_week ASC, tt.pair_number ASC
        """, (group_id,))
        return [dict(r) for r in cursor.fetchall()]

