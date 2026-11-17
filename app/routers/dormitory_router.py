from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
import datetime
from app.templates_helper import render
from app.auth import get_current_user, require_roles, log_activity
from app.database import get_db

router = APIRouter(prefix="/dormitory", tags=["dormitory"])

@router.get("", response_class=HTMLResponse)
async def dormitory_page(request: Request, current_user: dict = Depends(get_current_user)):
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT r.*, COUNT(dr.id) as occupied_count
            FROM dormitory_rooms r
            LEFT JOIN dormitory_residents dr ON dr.room_id = r.id AND dr.status = 'Yashamoqda'
            GROUP BY r.id
            ORDER BY r.building ASC, r.room_number ASC
        """)
        rooms = [dict(row) for row in cursor.fetchall()]

        cursor.execute("""
            SELECT dr.*, s.full_name as student_name, s.student_code, s.phone,
                   g.name as group_name, r.building, r.room_number
            FROM dormitory_residents dr
            JOIN students s ON dr.student_id = s.id
            JOIN groups g ON s.group_id = g.id
            JOIN dormitory_rooms r ON dr.room_id = r.id
            WHERE dr.status = 'Yashamoqda'
            ORDER BY dr.check_in_date DESC
        """)
        residents = [dict(row) for row in cursor.fetchall()]

        cursor.execute("""
            SELECT s.id, s.full_name, s.gender, g.name as group_name
            FROM students s
            JOIN groups g ON s.group_id = g.id
            WHERE s.status = 'O''qimoqda' AND s.id NOT IN (
                SELECT student_id FROM dormitory_residents WHERE status = 'Yashamoqda'
            )
            ORDER BY s.full_name ASC
        """)
        available_students = [dict(row) for row in cursor.fetchall()]

    current_date_iso = datetime.datetime.now().strftime("%Y-%m-%d")

    return render(request, "dormitory/index.html", {
        "current_user": current_user,
        "rooms": rooms,
        "residents": residents,
        "available_students": available_students,
        "current_date_iso": current_date_iso
    })

@router.post("/check-in")
async def check_in(
    student_id: int = Form(...),
    room_id: int = Form(...),
    check_in_date: str = Form(...),
    order_number: str = Form(""),
    current_user: dict = Depends(require_roles("admin", "dean"))
):
    with get_db() as conn:
        conn.execute("""
            INSERT INTO dormitory_residents (room_id, student_id, check_in_date, order_number, status)
            VALUES (?, ?, ?, ?, 'Yashamoqda')
        """, (room_id, student_id, check_in_date, order_number))
    log_activity(current_user["id"], current_user["full_name"], "DORMITORY_CHECK_IN", f"Talaba yotoqxonaga joylashtirildi: Student={student_id}, Room={room_id}")
    return RedirectResponse(url="/dormitory", status_code=status.HTTP_302_FOUND)

@router.post("/check-out/{resident_id}")
async def check_out(resident_id: int, current_user: dict = Depends(require_roles("admin", "dean"))):
    now = datetime.datetime.now().strftime("%Y-%m-%d")
    with get_db() as conn:
        conn.execute("""
            UPDATE dormitory_residents
            SET status = 'Chiqib ketgan', check_out_date = ?
            WHERE id = ?
        """, (now, resident_id))
    log_activity(current_user["id"], current_user["full_name"], "DORMITORY_CHECK_OUT", f"Talaba yotoqxonadan chiqarildi ID={resident_id}")
    return RedirectResponse(url="/dormitory", status_code=status.HTTP_302_FOUND)
