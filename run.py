import uvicorn
import os
import sys

def main():
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8000))

    print("=" * 65)
    print("  HEMIS - OLIY TA'LIM TALABALARINI BOSHQARISH AXBOROT TIZIMI")
    print("=" * 65)
    print(f"  Server manzili:      http://{host}:{port}")
    print(f"  Hujjatlar (Swagger): http://{host}:{port}/docs")
    print("-" * 65)
    print("  FOYDALANUVCHILAR VA PAROLLAR:")
    print("  1. Administrator:   admin       / admin123")
    print("  2. Dekanat:         dekan       / dekan123")
    print("  3. O'qituvchi:      teacher     / teacher123")
    print("  4. Talaba kabineti: 39522110001 / student123")
    print("=" * 65)
    print("  Server ishga tushirilmoqda...\n")

    uvicorn.run("app.main:app", host=host, port=port, reload=False)

if __name__ == "__main__":
    main()
