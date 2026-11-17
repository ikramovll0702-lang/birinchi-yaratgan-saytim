from fastapi import APIRouter, Request, Form, Response, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from app.templates_helper import render
from app.database import get_db
from app.auth import (
    hash_password, verify_password, sign_session_token,
    SESSION_COOKIE_NAME, get_current_user_optional, get_current_user,
    log_activity
)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    user = get_current_user_optional(request)
    if user:
        if user["role"] == "student":
            return RedirectResponse(url="/portal", status_code=status.HTTP_302_FOUND)
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    return render(request, "auth/login.html", {"current_user": None, "error": None})

@router.post("/login", response_class=HTMLResponse)
async def login_action(
    request: Request,
    response: Response,
    username: str = Form(...),
    password: str = Form(...)
):
    username = username.strip()
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password_hash, full_name, role FROM users WHERE LOWER(username) = LOWER(?)", (username,))
        user_row = cursor.fetchone()

    if not user_row or not verify_password(password, user_row["password_hash"]):
        return render(request, "auth/login.html", {
            "current_user": None,
            "error": "Login yoki parol noto'g'ri kiritildi!"
        }, status_code=status.HTTP_401_UNAUTHORIZED)

    token = sign_session_token(user_row["id"])
    redirect_url = "/portal" if user_row["role"] == "student" else "/dashboard"
    res = RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
    res.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=token,
        httponly=True,
        max_age=86400 * 7,
        samesite="lax"
    )
    log_activity(user_row["id"], user_row["full_name"], "LOGIN", f"Foydalanuvchi tizimga kirdi: {username}")
    return res

@router.get("/logout")
async def logout(request: Request):
    user = get_current_user_optional(request)
    if user:
        log_activity(user["id"], user["full_name"], "LOGOUT", "Tizimdan chiqdi")
    res = RedirectResponse(url="/auth/login", status_code=status.HTTP_302_FOUND)
    res.delete_cookie(SESSION_COOKIE_NAME)
    return res

@router.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request, current_user: dict = Depends(get_current_user)):
    return render(request, "auth/profile.html", {
        "current_user": current_user,
        "message": None,
        "error": None
    })

@router.post("/profile", response_class=HTMLResponse)
async def profile_change_password(
    request: Request,
    old_password: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...),
    current_user: dict = Depends(get_current_user)
):
    if new_password != confirm_password:
        return render(request, "auth/profile.html", {
            "current_user": current_user,
            "error": "Yangi parollar mos kelmadi!"
        })

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE id = ?", (current_user["id"],))
        row = cursor.fetchone()
        if not row or not verify_password(old_password, row["password_hash"]):
            return render(request, "auth/profile.html", {
                "current_user": current_user,
                "error": "Joriy parol noto'g'ri kiritildi!"
            })

        new_hash = hash_password(new_password)
        cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (new_hash, current_user["id"]))
        log_activity(current_user["id"], current_user["full_name"], "PASSWORD_CHANGE", "Parol yangilandi")

    return render(request, "auth/profile.html", {
        "current_user": current_user,
        "message": "Parolingiz muvaffaqiyatli o'zgartirildi!"
    })
