from typing import Tuple, Dict, Any, List
from app.database import get_db

def calculate_letter_and_gpa(total_score: float) -> Tuple[str, float]:
    """
    Kredit-modul tizimi (HEMIS) bo'yicha baholash shkalasi:
    90-100: A (4.0)
    85-89: B+ (3.5)
    80-84: B (3.0)
    75-79: C+ (2.5)
    70-74: C (2.0)
    60-69: D (1.0)
    0-59: F (0.0)
    """
    score = round(total_score, 1)
    if score >= 90:
        return "A", 4.0
    elif score >= 85:
        return "B+", 3.5
    elif score >= 80:
        return "B", 3.0
    elif score >= 75:
        return "C+", 2.5
    elif score >= 70:
        return "C", 2.0
    elif score >= 60:
        return "D", 1.0
    else:
        return "F", 0.0

def save_or_update_grade(student_id: int, subject_id: int, semester: int, academic_year: str,
                         current_grade: float, midterm_grade: float, final_grade: float) -> Dict[str, Any]:
    total_score = round(current_grade + midterm_grade + final_grade, 1)
    letter_grade, gpa_point = calculate_letter_and_gpa(total_score)
    status = "O'tdi" if total_score >= 60 else "Qarzdor"

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO grades (
                student_id, subject_id, semester, academic_year,
                current_grade, midterm_grade, final_grade,
                total_score, letter_grade, gpa_point, status, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now', 'localtime'))
            ON CONFLICT(student_id, subject_id, semester, academic_year) DO UPDATE SET
                current_grade = excluded.current_grade,
                midterm_grade = excluded.midterm_grade,
                final_grade = excluded.final_grade,
                total_score = excluded.total_score,
                letter_grade = excluded.letter_grade,
                gpa_point = excluded.gpa_point,
                status = excluded.status,
                updated_at = datetime('now', 'localtime');
        """, (student_id, subject_id, semester, academic_year,
              current_grade, midterm_grade, final_grade,
              total_score, letter_grade, gpa_point, status))
        
        return {
            "student_id": student_id,
            "subject_id": subject_id,
            "total_score": total_score,
            "letter_grade": letter_grade,
            "gpa_point": gpa_point,
            "status": status
        }

def calculate_student_gpa(student_id: int) -> float:
    """
    HEMIS GPA = Sum(Credit * GPA_Point) / Sum(Credits)
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.credits, g.gpa_point
            FROM grades g
            JOIN subjects s ON g.subject_id = s.id
            WHERE g.student_id = ? AND g.total_score > 0
        """, (student_id,))
        rows = cursor.fetchall()
        
        if not rows:
            return 0.0
        
        total_credits = 0
        weighted_points = 0.0
        for r in rows:
            creds = r["credits"]
            gp = r["gpa_point"]
            total_credits += creds
            weighted_points += (creds * gp)
            
        if total_credits == 0:
            return 0.0
        return round(weighted_points / total_credits, 2)

def get_student_transcript(student_id: int) -> List[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                g.id, g.semester, g.academic_year,
                s.code as subject_code, s.name as subject_name, s.credits, s.total_hours,
                g.current_grade, g.midterm_grade, g.final_grade,
                g.total_score, g.letter_grade, g.gpa_point, g.status
            FROM grades g
            JOIN subjects s ON g.subject_id = s.id
            WHERE g.student_id = ?
            ORDER BY g.semester ASC, s.name ASC
        """, (student_id,))
        return [dict(r) for r in cursor.fetchall()]

