import hashlib
import os
import secrets
import hmac
import time
from typing import Optional, Dict
from fastapi import Request, HTTPException, status, Depends
from fastapi.responses import RedirectResponse
from app.database import get_db

SECRET_KEY = os.environ.get("SECRET_KEY", "hemis_secure_session_key_uz_2026_super_secret")
SESSION_COOKIE_NAME = "hemis_session"
SESSION_EXPIRY_SECONDS = 86400 * 7 # 7 days

# In-memory session store (or we can use signed tokens)
# A signed token format: user_id:timestamp:hmac_signature
def sign_session_token(user_id: int) -> str:
    timestamp = int(time.time())
    payload = f"{user_id}:{timestamp}"
    signature = hmac.new(SECRET_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}:{signature}"

def verify_session_token(token: str) -> Optional[int]:
    if not token or ":" not in token:
        return None
    parts = token.split(":")
    if len(parts) != 3:
        return None
    user_id_str, timestamp_str, signature = parts
    try:
        user_id = int(user_id_str)
        timestamp = int(timestamp_str)
    except ValueError:
        return None
    
    # Check expiration
    if time.time() - timestamp > SESSION_EXPIRY_SECONDS:
        return None
    
    expected_payload = f"{user_id}:{timestamp}"
    expected_signature = hmac.new(SECRET_KEY.encode(), expected_payload.encode(), hashlib.sha256).hexdigest()
    if hmac.compare_digest(signature, expected_signature):
        return user_id
    return None

def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000).hex()
    return f"{salt}:{hashed}"

def verify_password(password: str, stored_hash: str) -> bool:
    if not stored_hash or ":" not in stored_hash:
        return False
    salt, hashed = stored_hash.split(":", 1)
    recalculated = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000).hex()
    return hmac.compare_digest(hashed, recalculated)

def get_current_user_optional(request: Request) -> Optional[Dict]:
    token = request.cookies.get(SESSION_COOKIE_NAME)
    if not token:
        return None
    user_id = verify_session_token(token)
    if not user_id:
        return None
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, full_name, role, email, phone, student_id, teacher_id, avatar_url FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            return dict(row)
    return None

def get_current_user(request: Request) -> Dict:
    user = get_current_user_optional(request)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            headers={"Location": "/auth/login"}
        )
    return user

def require_roles(*allowed_roles):
    def dependency(user: Dict = Depends(get_current_user)):
        if user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Ushbu sahifaga kirish huquqingiz yetarli emas!"
            )
        return user
    return dependency

def log_activity(user_id: Optional[int], user_name: Optional[str], action: str, details: str = "", ip_address: str = ""):
    try:
        with get_db() as conn:
            conn.execute(
                "INSERT INTO activity_logs (user_id, user_name, action, details, ip_address) VALUES (?, ?, ?, ?, ?)",
                (user_id, user_name, action, details, ip_address)
            )
    except Exception:
        pass

