import sqlite3
import os
from contextlib import contextmanager

DB_FILE = os.environ.get(
    "DB_PATH",
    os.environ.get(
        "DATABASE_PATH",
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "university.db")
    )
)
# Ensure the parent directory for DB exists (e.g. for mounted volumes like /data)
db_parent = os.path.dirname(os.path.abspath(DB_FILE))
if db_parent and not os.path.exists(db_parent):
    try:
        os.makedirs(db_parent, exist_ok=True)
    except Exception:
        pass

def get_db_connection():
    conn = sqlite3.connect(DB_FILE, timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

@contextmanager
def get_db():
    conn = get_db_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        
        # 1. Users
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'dean', 'teacher', 'student')),
            email TEXT,
            phone TEXT,
            student_id INTEGER,
            teacher_id INTEGER,
            avatar_url TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
        );
        """)

        # 2. Faculties
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS faculties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            dean_name TEXT,
            phone TEXT,
            description TEXT
        );
        """)

        # 3. Departments
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            faculty_id INTEGER NOT NULL REFERENCES faculties(id) ON DELETE CASCADE,
            name TEXT NOT NULL,
            head_name TEXT,
            phone TEXT
        );
        """)

        # 4. Specialties
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS specialties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            faculty_id INTEGER NOT NULL REFERENCES faculties(id) ON DELETE CASCADE,
            code TEXT NOT NULL,
            name TEXT NOT NULL,
            degree TEXT NOT NULL DEFAULT 'Bakalavriat',
            duration_years INTEGER DEFAULT 4
        );
        """)

        # 5. Academic Groups
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            faculty_id INTEGER NOT NULL REFERENCES faculties(id) ON DELETE CASCADE,
            specialty_id INTEGER NOT NULL REFERENCES specialties(id) ON DELETE CASCADE,
            course_level INTEGER NOT NULL CHECK(course_level BETWEEN 1 AND 6),
            academic_year TEXT NOT NULL DEFAULT '2025-2026',
            education_type TEXT NOT NULL DEFAULT 'Kunduzgi',
            language TEXT NOT NULL DEFAULT 'O''zbek',
            tutor_name TEXT
        );
        """)

        # 6. Students
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_code TEXT UNIQUE NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            middle_name TEXT,
            full_name TEXT NOT NULL,
            pinfl TEXT UNIQUE,
            passport_number TEXT,
            birth_date TEXT,
            gender TEXT NOT NULL DEFAULT 'Erkak',
            nationality TEXT DEFAULT 'O''zbek',
            phone TEXT,
            email TEXT,
            address TEXT,
            region TEXT,
            district TEXT,
            parent_phone TEXT,
            group_id INTEGER NOT NULL REFERENCES groups(id) ON DELETE RESTRICT,
            faculty_id INTEGER NOT NULL REFERENCES faculties(id) ON DELETE RESTRICT,
            specialty_id INTEGER NOT NULL REFERENCES specialties(id) ON DELETE RESTRICT,
            payment_form TEXT NOT NULL DEFAULT 'To''lov-shartnoma',
            education_type TEXT NOT NULL DEFAULT 'Kunduzgi',
            education_degree TEXT NOT NULL DEFAULT 'Bakalavr',
            course_level INTEGER NOT NULL DEFAULT 1,
            admission_year INTEGER NOT NULL DEFAULT 2024,
            status TEXT NOT NULL DEFAULT 'O''qimoqda',
            photo_url TEXT,
            notes TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
        );
        """)

        # 7. Teachers
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            department_id INTEGER NOT NULL REFERENCES departments(id) ON DELETE CASCADE,
            academic_degree TEXT DEFAULT 'Assistent',
            phone TEXT,
            email TEXT,
            status TEXT DEFAULT 'Faol'
        );
        """)

        # 8. Subjects
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL,
            name TEXT NOT NULL,
            department_id INTEGER NOT NULL REFERENCES departments(id) ON DELETE CASCADE,
            credits INTEGER NOT NULL DEFAULT 4,
            total_hours INTEGER NOT NULL DEFAULT 120,
            lecture_hours INTEGER DEFAULT 30,
            practice_hours INTEGER DEFAULT 30,
            lab_hours INTEGER DEFAULT 0,
            independent_hours INTEGER DEFAULT 60,
            semester INTEGER NOT NULL DEFAULT 1
        );
        """)

        # 9. Group Subjects
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS group_subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id INTEGER NOT NULL REFERENCES groups(id) ON DELETE CASCADE,
            subject_id INTEGER NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
            teacher_id INTEGER REFERENCES teachers(id) ON DELETE SET NULL,
            semester INTEGER NOT NULL,
            academic_year TEXT NOT NULL DEFAULT '2025-2026',
            UNIQUE(group_id, subject_id, semester, academic_year)
        );
        """)

        # 10. Grades (Kredit-modul tizimi)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
            subject_id INTEGER NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
            semester INTEGER NOT NULL,
            academic_year TEXT NOT NULL DEFAULT '2025-2026',
            current_grade REAL DEFAULT 0,
            midterm_grade REAL DEFAULT 0,
            final_grade REAL DEFAULT 0,
            total_score REAL DEFAULT 0,
            letter_grade TEXT DEFAULT 'F',
            gpa_point REAL DEFAULT 0.0,
            status TEXT DEFAULT 'Kiritildi',
            updated_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
            UNIQUE(student_id, subject_id, semester, academic_year)
        );
        """)

        # 11. Attendance
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
            subject_id INTEGER NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
            group_id INTEGER NOT NULL REFERENCES groups(id) ON DELETE CASCADE,
            date TEXT NOT NULL,
            pair_number INTEGER NOT NULL DEFAULT 1,
            status TEXT NOT NULL CHECK(status IN ('Bor', 'Sababli', 'Sababsiz')),
            hours INTEGER NOT NULL DEFAULT 2,
            notes TEXT,
            UNIQUE(student_id, subject_id, date, pair_number)
        );
        """)

        # 12. Contracts & Payments
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS contracts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
            academic_year TEXT NOT NULL DEFAULT '2025-2026',
            contract_number TEXT UNIQUE NOT NULL,
            total_amount REAL NOT NULL,
            paid_amount REAL DEFAULT 0,
            discount_amount REAL DEFAULT 0,
            due_date TEXT,
            status TEXT NOT NULL DEFAULT 'Qarzdor',
            created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
        );
        """)

        # 13. Payments History
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contract_id INTEGER NOT NULL REFERENCES contracts(id) ON DELETE CASCADE,
            student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
            amount REAL NOT NULL,
            payment_date TEXT NOT NULL,
            payment_method TEXT DEFAULT 'Bank o''tkazmasi',
            receipt_number TEXT,
            notes TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
        );
        """)

        # 14. Dormitory Rooms & Residents
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS dormitory_rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            building TEXT NOT NULL,
            room_number TEXT NOT NULL,
            floor INTEGER NOT NULL,
            capacity INTEGER NOT NULL DEFAULT 4,
            gender TEXT NOT NULL DEFAULT 'Erkak',
            monthly_price REAL DEFAULT 150000,
            status TEXT DEFAULT 'Bo''sh'
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS dormitory_residents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_id INTEGER NOT NULL REFERENCES dormitory_rooms(id) ON DELETE CASCADE,
            student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
            check_in_date TEXT NOT NULL,
            check_out_date TEXT,
            order_number TEXT,
            status TEXT DEFAULT 'Yashamoqda'
        );
        """)

        # 15. Timetables
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS timetables (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id INTEGER NOT NULL REFERENCES groups(id) ON DELETE CASCADE,
            subject_id INTEGER NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
            teacher_id INTEGER NOT NULL REFERENCES teachers(id) ON DELETE CASCADE,
            day_of_week INTEGER NOT NULL CHECK(day_of_week BETWEEN 1 AND 6),
            pair_number INTEGER NOT NULL CHECK(pair_number BETWEEN 1 AND 6),
            room_number TEXT NOT NULL,
            lesson_type TEXT NOT NULL DEFAULT 'Ma''ruza'
        );
        """)

        # 16. System Activity Logs
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS activity_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            user_name TEXT,
            action TEXT NOT NULL,
            details TEXT,
            ip_address TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
        );
        """)

        # Indexes for fast search and joins
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_students_group ON students(group_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_students_faculty ON students(faculty_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_students_code ON students(student_code);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_students_name ON students(full_name);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_grades_student ON grades(student_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_attendance_student ON attendance(student_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_contracts_student ON contracts(student_id);")
