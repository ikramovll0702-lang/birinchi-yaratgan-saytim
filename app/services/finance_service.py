from typing import List, Dict, Any, Optional
from app.database import get_db

def get_contracts(status: Optional[str] = None, faculty_id: Optional[int] = None, search: Optional[str] = None) -> List[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            SELECT c.*, 
                   s.full_name as student_name, s.student_code, s.phone as student_phone,
                   g.name as group_name, f.name as faculty_name,
                   (c.total_amount - c.paid_amount - c.discount_amount) as remaining_amount
            FROM contracts c
            JOIN students s ON c.student_id = s.id
            JOIN groups g ON s.group_id = g.id
            JOIN faculties f ON s.faculty_id = f.id
            WHERE 1=1
        """
        params = []
        if status:
            query += " AND c.status = ?"
            params.append(status)
        if faculty_id:
            query += " AND s.faculty_id = ?"
            params.append(faculty_id)
        if search:
            query += " AND (s.full_name LIKE ? OR s.student_code LIKE ? OR c.contract_number LIKE ?)"
            val = f"%{search.strip()}%"
            params.extend([val, val, val])

        query += " ORDER BY remaining_amount DESC, c.id DESC"
        cursor.execute(query, params)
        return [dict(r) for r in cursor.fetchall()]

def record_payment(contract_id: int, student_id: int, amount: float, payment_date: str, payment_method: str = "Bank o'tkazmasi", receipt_number: str = "", notes: str = ""):
    with get_db() as conn:
        cursor = conn.cursor()
        # Insert payment record
        cursor.execute("""
            INSERT INTO payments (contract_id, student_id, amount, payment_date, payment_method, receipt_number, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (contract_id, student_id, amount, payment_date, payment_method, receipt_number, notes))

        # Update contract paid amount and status
        cursor.execute("SELECT total_amount, paid_amount, discount_amount FROM contracts WHERE id = ?", (contract_id,))
        contract = cursor.fetchone()
        if contract:
            new_paid = contract["paid_amount"] + amount
            new_status = "To'langan" if new_paid + contract["discount_amount"] >= contract["total_amount"] else "Qisman to'langan"
            cursor.execute("""
                UPDATE contracts 
                SET paid_amount = ?, status = ?
                WHERE id = ?
            """, (new_paid, new_status, contract_id))

def get_payments_for_student(student_id: int) -> List[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.*, c.contract_number
            FROM payments p
            JOIN contracts c ON p.contract_id = c.id
            WHERE p.student_id = ?
            ORDER BY p.payment_date DESC, p.id DESC
        """, (student_id,))
        return [dict(r) for r in cursor.fetchall()]

def get_finance_overview() -> Dict[str, Any]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                COUNT(*) as total_contracts,
                SUM(total_amount) as total_expected,
                SUM(paid_amount) as total_received,
                SUM(discount_amount) as total_discounts,
                SUM(CASE WHEN status = 'Qarzdor' THEN 1 ELSE 0 END) as debtor_count,
                SUM(CASE WHEN status = 'To''langan' THEN 1 ELSE 0 END) as fully_paid_count,
                SUM(CASE WHEN status = 'Qisman to''langan' THEN 1 ELSE 0 END) as partially_paid_count
            FROM contracts
        """)
        row = cursor.fetchone()
        data = dict(row) if row else {}
        total_exp = data.get("total_expected") or 0
        total_rec = data.get("total_received") or 0
        data["total_debt"] = max(0, total_exp - total_rec - (data.get("total_discounts") or 0))
        return data

