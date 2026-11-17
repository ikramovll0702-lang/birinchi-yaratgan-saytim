import uvicorn
import os
import sys

def main():
    print("=" * 65)
    print("  HEMIS - OLIY TA'LIM TALABALARINI BOSHQARISH AXBOROT TIZIMI")
    print("=" * 65)
    print("  Server manzili:      http://127.0.0.1:8000")
    print("  Hujjatlar (Swagger): http://127.0.0.1:8000/docs")
    print("-" * 65)
    print("  FOYDALANUVCHILAR VA PAROLLAR:")
    print("  1. Administrator:   admin       / admin123")
    print("  2. Dekanat:         dekan       / dekan123")
    print("  3. O'qituvchi:      teacher     / teacher123")
    print("  4. Talaba kabineti: 39522110001 / student123")
    print("=" * 65)
    print("  Server ishga tushirilmoqda...\n")

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)

if __name__ == "__main__":
    main()

