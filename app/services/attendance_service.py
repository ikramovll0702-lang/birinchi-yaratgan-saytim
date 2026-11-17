from typing import List, Dict, Any, Optional
from app.database import get_db

def mark_attendance(student_id: int, subject_id: int, group_id: int, date: str, pair_number: int, status: str, hours: int = 2, notes: str = ""):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO attendance (student_id, subject_id, group_id, date, pair_number, status, hours, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(student_id, subject_id, date, pair_number) DO UPDATE SET
                status = excluded.status,
                hours = excluded.hours,
                notes = excluded.notes;
        """, (student_id, subject_id, group_id, date, pair_number, status, hours, notes))

def get_group_attendance_for_date(group_id: int, subject_id: int, date: str, pair_number: int) -> List[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.id as student_id, s.full_name, s.student_code,
                   COALESCE(a.status, 'Bor') as status,
                   COALESCE(a.hours, 2) as hours,
                   COALESCE(a.notes, '') as notes
            FROM students s
            LEFT JOIN attendance a ON a.student_id = s.id AND a.subject_id = ? AND a.date = ? AND a.pair_number = ?
            WHERE s.group_id = ? AND s.status = 'O''qimoqda'
            ORDER BY s.full_name ASC
        """, (subject_id, date, pair_number, group_id))
        return [dict(r) for r in cursor.fetchall()]

def get_student_attendance_history(student_id: int) -> List[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.*, s.name as subject_name
            FROM attendance a
            JOIN subjects s ON a.subject_id = s.id
            WHERE a.student_id = ?
            ORDER BY a.date DESC, a.pair_number ASC
        """, (student_id,))
        return [dict(r) for r in cursor.fetchall()]

def get_attendance_warnings(threshold_hours: int = 74) -> List[Dict[str, Any]]:
    """
    HEMIS qoidasi: 74 soatdan ortiq sababsiz dars qoldirgan talabalar ogohlantiriladi / chetlatiladi.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.id, s.student_code, s.full_name, s.phone,
                   g.name as group_name, f.name as faculty_name,
                   SUM(CASE WHEN a.status = 'Sababsiz' THEN a.hours ELSE 0 END) as unexcused_hours,
                   SUM(CASE WHEN a.status = 'Sababli' THEN a.hours ELSE 0 END) as excused_hours,
                   SUM(a.hours) as total_missed_hours
            FROM students s
            JOIN groups g ON s.group_id = g.id
            JOIN faculties f ON s.faculty_id = f.id
            JOIN attendance a ON a.student_id = s.id
            WHERE s.status = 'O''qimoqda'
            GROUP BY s.id
            HAVING unexcused_hours >= ?
            ORDER BY unexcused_hours DESC
        """, (threshold_hours,))
        return [dict(r) for r in cursor.fetchall()]

