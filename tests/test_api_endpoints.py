import pytest
from starlette.testclient import TestClient
from app.main import app
from app.auth import sign_session_token, SESSION_COOKIE_NAME

client = TestClient(app)

def test_login_page_loads():
    response = client.get("/auth/login")
    assert response.status_code == 200
    assert "HEMIS Axborot Tizimi" in response.text

def test_login_flow():
    # Attempt invalid password
    res_fail = client.post("/auth/login", data={"username": "admin", "password": "wrongpassword"})
    assert res_fail.status_code == 401

    # Valid admin login
    res_ok = client.post("/auth/login", data={"username": "admin", "password": "admin123"}, follow_redirects=False)
    assert res_ok.status_code == 302
    assert SESSION_COOKIE_NAME in res_ok.cookies

def test_dashboard_with_authenticated_user():
    token = sign_session_token(1) # Admin user
    client.cookies.set(SESSION_COOKIE_NAME, token)
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert "Boshqaruv Markazi" in response.text
    assert "Jami Talabalar" in response.text

def test_students_list_and_detail():
    token = sign_session_token(1)
    client.cookies.set(SESSION_COOKIE_NAME, token)
    
    # List
    res_list = client.get("/students")
    assert res_list.status_code == 200
    assert "Talabalar Bazasi" in res_list.text

    # Detail
    res_detail = client.get("/students/1")
    assert res_detail.status_code == 200
    assert "Shaxsiy Ma'lumotlar" in res_detail.text
    assert "Transkript" in res_detail.text

def test_pdf_endpoints():
    token = sign_session_token(1)
    client.cookies.set(SESSION_COOKIE_NAME, token)

    res_cert = client.get("/students/1/certificate.pdf")
    assert res_cert.status_code == 200
    assert res_cert.headers["content-type"] == "application/pdf"
    assert res_cert.content.startswith(b"%PDF")

    res_trans = client.get("/students/1/transcript.pdf")
    assert res_trans.status_code == 200
    assert res_trans.headers["content-type"] == "application/pdf"
    assert res_trans.content.startswith(b"%PDF")

    res_id = client.get("/students/1/id-card.pdf")
    assert res_id.status_code == 200
    assert res_id.headers["content-type"] == "application/pdf"
    assert res_id.content.startswith(b"%PDF")

def test_excel_export_endpoint():
    token = sign_session_token(1)
    client.cookies.set(SESSION_COOKIE_NAME, token)
    res_excel = client.get("/students/export/excel")
    assert res_excel.status_code == 200
    assert "spreadsheetml.sheet" in res_excel.headers["content-type"]

def test_academics_and_timetable_endpoints():
    token = sign_session_token(1)
    client.cookies.set(SESSION_COOKIE_NAME, token)

    res_sub = client.get("/academics/subjects")
    assert res_sub.status_code == 200
    assert "O'quv Rejasidagi Fanlar" in res_sub.text

    res_tt = client.get("/academics/timetable")
    assert res_tt.status_code == 200
    assert "Dars Jadvali" in res_tt.text

def test_grades_and_attendance_endpoints():
    token = sign_session_token(1)
    client.cookies.set(SESSION_COOKIE_NAME, token)

    res_grades = client.get("/grades")
    assert res_grades.status_code == 200
    assert "Kredit-Modul Baholash Jurnali" in res_grades.text

    res_att = client.get("/attendance")
    assert res_att.status_code == 200
    assert "Davomat Qaydnomasi" in res_att.text

    res_warn = client.get("/attendance/warnings")
    assert res_warn.status_code == 200
    assert "74+ Soat" in res_warn.text

def test_finance_and_dormitory_endpoints():
    token = sign_session_token(1)
    client.cookies.set(SESSION_COOKIE_NAME, token)

    res_fin = client.get("/finance")
    assert res_fin.status_code == 200
    assert "To'lov-Shartnomalar" in res_fin.text

    res_dorm = client.get("/dormitory")
    assert res_dorm.status_code == 200
    assert "Talabalar Turar Joyi" in res_dorm.text

def test_student_portal_endpoint():
    # Student login (student user id for 39522110001 is student_id=1)
    token = sign_session_token(4) # Student user
    client.cookies.set(SESSION_COOKIE_NAME, token)

    res_portal = client.get("/portal")
    assert res_portal.status_code == 200
    assert "Talaba Portali" in res_portal.text
    assert "Mening Baholarim" in res_portal.text

def test_json_api_endpoints():
    res_opts = client.get("/api/faculty/1/options")
    assert res_opts.status_code == 200
    json_data = res_opts.json()
    assert "specialties" in json_data
    assert "groups" in json_data

    res_search = client.get("/api/students/search?q=Sardor")
    assert res_search.status_code == 200
    search_data = res_search.json()
    assert search_data["total"] >= 1

