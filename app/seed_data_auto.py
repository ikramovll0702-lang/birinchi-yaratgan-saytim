from app.database import get_db

def ensure_initial_seed():
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            if count == 0:
                print("Ma'lumotlar bazasi bo'sh. Demo ma'lumotlar kiritilmoqda...")
                from seed_data import seed_database
                seed_database()
    except Exception as e:
        print(f"Boshlang'ich ma'lumotlarni tekshirishda xatolik: {e}")

