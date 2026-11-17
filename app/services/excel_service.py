import io
import random
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from app.database import get_db
from app.services.student_service import create_student

def export_students_to_excel(students: list) -> io.BytesIO:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Talabalar ro'yxati"

    # Header style
    header_fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    align_left = Alignment(horizontal="left", vertical="center")
    
    thin_border = Border(
        left=Side(style='thin', color='CBD5E1'),
        right=Side(style='thin', color='CBD5E1'),
        top=Side(style='thin', color='CBD5E1'),
        bottom=Side(style='thin', color='CBD5E1')
    )

    headers = [
        "№", "Talaba ID", "F.I.Sh.", "JSHSHIR", "Pasport",
        "Fakultet", "Yo'nalish", "Guruh", "Kurs",
        "Ta'lim shakli", "To'lov turi", "GPA", "Telefon", "Holati"
    ]

    ws.append(headers)
    for col_num in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col_num)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = align_center
        cell.border = thin_border

    # Data rows
    for idx, st in enumerate(students, 1):
        row = [
            idx,
            st.get("student_code", ""),
            st.get("full_name", ""),
            st.get("pinfl", ""),
            st.get("passport_number", ""),
            st.get("faculty_name", ""),
            st.get("specialty_name", ""),
            st.get("group_name", ""),
            st.get("course_level", 1),
            st.get("education_type", ""),
            st.get("payment_form", ""),
            st.get("gpa", 0.0),
            st.get("phone", ""),
            st.get("status", "")
        ]
        ws.append(row)
        current_row = idx + 1
        for col_num in range(1, len(row) + 1):
            cell = ws.cell(row=current_row, column=col_num)
            cell.border = thin_border
            cell.font = Font(name="Calibri", size=10)
            if col_num in [1, 2, 4, 5, 9, 12, 14]:
                cell.alignment = align_center
            else:
                cell.alignment = align_left

    # Auto-adjust column width
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val_str = str(cell.value or "")
            if len(val_str) > max_len:
                max_len = len(val_str)
        ws.column_dimensions[col_letter].width = max(max_len + 3, 11)

    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer

def generate_sample_import_template() -> io.BytesIO:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Talaba_shablon"

    header_fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")

    headers = [
        "Familiya", "Ism", "Otasining ismi", "JSHSHIR", "Pasport",
        "Tug'ilgan sana (YYYY-MM-DD)", "Jinsi (Erkak/Ayol)", "Telefon", "Email",
        "Guruh ID", "Fakultet ID", "Yo'nalish ID", "To'lov shakli (Davlat granti / To'lov-shartnoma)",
        "Kurs (1-4)"
    ]
    ws.append(headers)
    for col_num in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col_num)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")

    sample_row = [
        "Karimov", "Anvar", "Rustamovich", "30101990010022", "AA1234567",
        "2002-05-15", "Erkak", "+998901234567", "anvar@example.uz",
        1, 1, 1, "To'lov-shartnoma",
        1
    ]
    ws.append(sample_row)

    for col in ws.columns:
        col_letter = get_column_letter(col[0].column)
        ws.column_dimensions[col_letter].width = 20

    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer

def import_students_from_excel(file_bytes: bytes) -> dict:
    wb = openpyxl.load_workbook(io.BytesIO(file_bytes), data_only=True)
    ws = wb.active

    imported = 0
    errors = []

    rows = list(ws.iter_rows(values_only=True))
    if len(rows) < 2:
        return {"success": False, "count": 0, "errors": ["Faylda ma'lumot topilmadi"]}

    for row_idx, r in enumerate(rows[1:], start=2):
        if not r or not r[0] or not r[1]:
            continue
        try:
            last_name = str(r[0]).strip()
            first_name = str(r[1]).strip()
            middle_name = str(r[2]).strip() if len(r) > 2 and r[2] else ""
            pinfl = str(r[3]).strip() if len(r) > 3 and r[3] else ""
            passport = str(r[4]).strip() if len(r) > 4 and r[4] else ""
            birth_date = str(r[5]).strip() if len(r) > 5 and r[5] else "2003-01-01"
            gender = str(r[6]).strip() if len(r) > 6 and r[6] else "Erkak"
            phone = str(r[7]).strip() if len(r) > 7 and r[7] else ""
            email = str(r[8]).strip() if len(r) > 8 and r[8] else ""
            
            group_id = int(r[9]) if len(r) > 9 and r[9] else 1
            faculty_id = int(r[10]) if len(r) > 10 and r[10] else 1
            specialty_id = int(r[11]) if len(r) > 11 and r[11] else 1
            payment_form = str(r[12]).strip() if len(r) > 12 and r[12] else "To'lov-shartnoma"
            course_level = int(r[13]) if len(r) > 13 and r[13] else 1

            if pinfl:
                with get_db() as conn:
                    cur = conn.cursor()
                    cur.execute("SELECT id FROM students WHERE pinfl = ?", (pinfl,))
                    if cur.fetchone():
                        pinfl = f"{pinfl[:10]}{random.randint(1000, 9999)}"

            student_data = {
                "first_name": first_name,
                "last_name": last_name,
                "middle_name": middle_name,
                "pinfl": pinfl,
                "passport_number": passport,
                "birth_date": birth_date,
                "gender": gender,
                "phone": phone,
                "email": email,
                "group_id": group_id,
                "faculty_id": faculty_id,
                "specialty_id": specialty_id,
                "payment_form": payment_form,
                "course_level": course_level,
                "education_type": "Kunduzgi",
                "education_degree": "Bakalavr",
                "admission_year": 2024,
                "status": "O'qimoqda"
            }
            create_student(student_data)
            imported += 1
        except Exception as e:
            errors.append(f"Qator {row_idx}: {str(e)}")

    return {
        "success": True,
        "count": imported,
        "errors": errors
    }
