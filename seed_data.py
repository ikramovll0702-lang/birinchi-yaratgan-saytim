import random
from app.database import init_db, get_db
from app.auth import hash_password
from app.services.grade_service import calculate_letter_and_gpa

def seed_database():
    print("Initsializatsiya qilinmoqda...")
    init_db()

    with get_db() as conn:
        cursor = conn.cursor()

        # Check if already seeded
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] > 0:
            print("Ma'lumotlar bazasi allaqachon to'ldirilgan.")
            return

        print("Foydalanuvchilar va ma'murlar yaratilmoqda...")
        # 1. Users
        users = [
            ("admin", hash_password("admin123"), "Tizim Administratori", "admin", "admin@edu.uz", "+998712000001"),
            ("dekan", hash_password("dekan123"), "Prof. Ravshan Aliyev", "dean", "dekan@edu.uz", "+998712000002"),
            ("teacher", hash_password("teacher123"), "Dots. Dilshod To'xtayev", "teacher", "teacher@edu.uz", "+998712000003"),
        ]
        cursor.executemany("""
            INSERT INTO users (username, password_hash, full_name, role, email, phone)
            VALUES (?, ?, ?, ?, ?, ?)
        """, users)

        # 2. Faculties
        print("Fakultetlar qo'shilmoqda...")
        faculties = [
            ("RTSI", "Raqamli texnologiyalar va sun'iy intellekt fakulteti", "Prof. Ravshan Aliyev", "+998712001100", "Axborot texnologiyalari va AI sohasidagi yetakchi fakultet"),
            ("IQM", "Iqtisodiyot va moliya fakulteti", "Dots. Nodira Karimova", "+998712001101", "Zamonaviy raqamli iqtisodiyot va bank ishi mutaxassislari"),
            ("MBT", "Muhandislik va biotibbiyot texnologiyalari fakulteti", "Prof. Botir Zokirov", "+998712001102", "Biotibbiyot, elektronika va avtomatlashtirish")
        ]
        cursor.executemany("""
            INSERT INTO faculties (code, name, dean_name, phone, description)
            VALUES (?, ?, ?, ?, ?)
        """, faculties)

        # 3. Departments
        print("Kafedralar qo'shilmoqda...")
        departments = [
            (1, "Dasturiy injiniring kafedrasi", "Dots. Dilshod To'xtayev", "+998712002201"),
            (1, "Sun'iy intellekt va algoritmlar kafedrasi", "PhD Jasur Fayzullayev", "+998712002202"),
            (1, "Axborot xavfsizligi kafedrasi", "Prof. Akmal Qodirov", "+998712002203"),
            (2, "Moliya va moliyaviy texnologiyalar kafedrasi", "Dots. Sarvar Bekmirzayev", "+998712002204"),
            (2, "Raqamli iqtisodiyot kafedrasi", "PhD Umida Rahimova", "+998712002205"),
            (3, "Biotibbiyot muhandisligi kafedrasi", "Prof. Mansur Yusupov", "+998712002206"),
        ]
        cursor.executemany("""
            INSERT INTO departments (faculty_id, name, head_name, phone)
            VALUES (?, ?, ?, ?)
        """, departments)

        # 4. Specialties
        print("Yo'nalishlar qo'shilmoqda...")
        specialties = [
            (1, "60610200", "Dasturiy injiniring", "Bakalavriat", 4),
            (1, "60610100", "Kompyuter injiniringi", "Bakalavriat", 4),
            (1, "60610500", "Sun'iy intellekt va ma'lumotlar tahlili", "Bakalavriat", 4),
            (2, "60410100", "Iqtisodiyot (raqamli iqtisodiyot)", "Bakalavriat", 4),
            (2, "60410400", "Moliya va moliyaviy texnologiyalar", "Bakalavriat", 4),
            (3, "60711400", "Biotibbiyot muhandisligi", "Bakalavriat", 4),
        ]
        cursor.executemany("""
            INSERT INTO specialties (faculty_id, code, name, degree, duration_years)
            VALUES (?, ?, ?, ?, ?)
        """, specialties)

        # 5. Groups
        print("Akademik guruhlar yaratilmoqda...")
        groups = [
            ("DI-22-01", 1, 1, 3, "2025-2026", "Kunduzgi", "O'zbek", "D. To'xtayev"),
            ("KI-23-02", 1, 2, 2, "2025-2026", "Kunduzgi", "O'zbek", "J. Fayzullayev"),
            ("SI-24-01", 1, 3, 1, "2025-2026", "Kunduzgi", "Ingliz", "A. Qodirov"),
            ("IQ-22-03", 2, 4, 3, "2025-2026", "Kunduzgi", "O'zbek", "S. Bekmirzayev"),
            ("MF-23-01", 2, 5, 2, "2025-2026", "Kunduzgi", "O'zbek", "U. Rahimova"),
            ("BM-24-01", 3, 6, 1, "2025-2026", "Kunduzgi", "O'zbek", "M. Yusupov"),
            ("DI-24-02", 1, 1, 1, "2025-2026", "Kechki", "O'zbek", "N. Soliyev"),
            ("KI-21-01", 1, 2, 4, "2025-2026", "Sirtqi", "O'zbek", "O. Bozorov"),
        ]
        cursor.executemany("""
            INSERT INTO groups (name, faculty_id, specialty_id, course_level, academic_year, education_type, language, tutor_name)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, groups)

        # 6. Teachers
        print("O'qituvchilar qo'shilmoqda...")
        teachers = [
            ("Dots. Dilshod To'xtayev", 1, "Dotsent", "+998901112233", "dilshod@edu.uz"),
            ("PhD Jasur Fayzullayev", 2, "PhD", "+998902223344", "jasur@edu.uz"),
            ("Prof. Akmal Qodirov", 3, "Professor", "+998903334455", "akmal@edu.uz"),
            ("Dots. Sarvar Bekmirzayev", 4, "Dotsent", "+998904445566", "sarvar@edu.uz"),
            ("PhD Umida Rahimova", 5, "PhD", "+998905556677", "umida@edu.uz"),
            ("Prof. Mansur Yusupov", 6, "Professor", "+998906667788", "mansur@edu.uz"),
            ("Katta o'qit. Nigora Soliyeva", 1, "Katta o'qituvchi", "+998907778899", "nigora@edu.uz"),
            ("Assistent Oybek Bozorov", 2, "Assistent", "+998908889900", "oybek@edu.uz"),
        ]
        cursor.executemany("""
            INSERT INTO teachers (full_name, department_id, academic_degree, phone, email)
            VALUES (?, ?, ?, ?, ?)
        """, teachers)

        # 7. Subjects
        print("Fanlar ro'yxati shakllantirilmoqda...")
        subjects = [
            ("SE301", "Dasturiy ta'minot muhandisligi", 1, 6, 180, 40, 40, 20, 80, 5),
            ("CS202", "Algoritmlar va ma'lumotlar tuzilmasi", 1, 5, 150, 36, 36, 0, 78, 3),
            ("DB201", "Ma'lumotlar bazasi tizimlari", 1, 5, 150, 30, 30, 20, 70, 3),
            ("AI301", "Sun'iy intellekt asoslari", 2, 6, 180, 40, 40, 20, 80, 5),
            ("ML302", "Mashinali o'rganish", 2, 5, 150, 30, 30, 20, 70, 4),
            ("SEC301", "Kiberxavfsizlik asoslari", 3, 5, 150, 30, 30, 20, 70, 4),
            ("FIN201", "Moliya va moliyaviy bozorlar", 4, 5, 150, 36, 36, 0, 78, 3),
            ("ECN202", "Ekonometrika va tahlil", 5, 5, 150, 36, 36, 0, 78, 3),
            ("MED101", "Biotibbiyot asoslari", 6, 4, 120, 30, 30, 0, 60, 1),
            ("MATH101", "Oliy matematika", 2, 6, 180, 50, 50, 0, 80, 1),
            ("ENG101", "Akademik ingliz tili", 1, 4, 120, 20, 40, 0, 60, 1),
            ("WEB201", "Web dasturlash texnologiyalari", 1, 5, 150, 30, 40, 10, 70, 3),
        ]
        cursor.executemany("""
            INSERT INTO subjects (code, name, department_id, credits, total_hours, lecture_hours, practice_hours, lab_hours, independent_hours, semester)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, subjects)

        # 8. Dormitory Rooms
        print("Yotoqxona xonalari yaratilmoqda...")
        rooms = [
            ("1-Bino", "101", 1, 4, "Erkak", 150000, "Band"),
            ("1-Bino", "102", 1, 4, "Erkak", 150000, "Bo'sh"),
            ("1-Bino", "201", 2, 3, "Ayol", 160000, "Band"),
            ("1-Bino", "202", 2, 3, "Ayol", 160000, "Bo'sh"),
            ("2-Bino", "301", 3, 4, "Erkak", 140000, "Band"),
            ("2-Bino", "302", 3, 4, "Erkak", 140000, "Bo'sh"),
        ]
        cursor.executemany("""
            INSERT INTO dormitory_rooms (building, room_number, floor, capacity, gender, monthly_price, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, rooms)

        # 9. Realistic Students Data
        print("Talabalar qo'shilmoqda (30+ talaba)...")
        uzbek_students = [
            # Group 1: DI-22-01 (Faculty 1, Specialty 1, Course 3)
            ("39522110001", "Sardor", "Nazarov", "Olim o'g'li", "31204015600011", "AC1234567", "2003-04-12", "Erkak", "+998901230001", "sardor.n@edu.uz", "Toshkent shahri, Chilonzor tumani", "Toshkent shahri", "Chilonzor", "+998901110001", 1, 1, 1, "Davlat granti", "Kunduzgi", "Bakalavr", 3, 2022, "O'qimoqda"),
            ("39522110002", "Madina", "Karimova", "Rustam qizi", "41508025600022", "AB7654321", "2003-08-15", "Ayol", "+998901230002", "madina.k@edu.uz", "Samarqand viloyati, Pastdarg'om tumani", "Samarqand viloyati", "Pastdarg'om", "+998901110002", 1, 1, 1, "To'lov-shartnoma", "Kunduzgi", "Bakalavr", 3, 2022, "O'qimoqda"),
            ("39522110003", "Javohir", "Sobirov", "Bahodir o'g'li", "30511015600033", "AA9876543", "2002-11-05", "Erkak", "+998901230003", "javohir.s@edu.uz", "Farg'ona viloyati, Qo'qon shahri", "Farg'ona viloyati", "Qo'qon", "+998901110003", 1, 1, 1, "To'lov-shartnoma", "Kunduzgi", "Bakalavr", 3, 2022, "O'qimoqda"),
            ("39522110004", "Shahzoda", "Alimova", "Anvar qizi", "42001025600044", "FA1122334", "2003-01-20", "Ayol", "+998901230004", "shahzoda.a@edu.uz", "Buxoro viloyati, G'ijduvon tumani", "Buxoro viloyati", "G'ijduvon", "+998901110004", 1, 1, 1, "Davlat granti", "Kunduzgi", "Bakalavr", 3, 2022, "O'qimoqda"),
            ("39522110005", "Bobur", "Tursunov", "Shavkat o'g'li", "31707015600055", "KA5544332", "2003-07-17", "Erkak", "+998901230005", "bobur.t@edu.uz", "Qashqadaryo viloyati, Qarshi shahri", "Qashqadaryo viloyati", "Qarshi", "+998901110005", 1, 1, 1, "To'lov-shartnoma", "Kunduzgi", "Bakalavr", 3, 2022, "O'qimoqda"),
            
            # Group 2: KI-23-02 (Faculty 1, Specialty 2, Course 2)
            ("39523110006", "Azizbek", "Qodirov", "Farxod o'g'li", "32509035600066", "AD4455667", "2004-09-25", "Erkak", "+998901230006", "azizbek.q@edu.uz", "Andijon viloyati, Asaka tumani", "Andijon viloyati", "Asaka", "+998901110006", 2, 1, 2, "Davlat granti", "Kunduzgi", "Bakalavr", 2, 2023, "O'qimoqda"),
            ("39523110007", "Dilnoza", "Yo'ldosheva", "Akram qizi", "40803035600077", "AE9988776", "2004-03-08", "Ayol", "+998901230007", "dilnoza.y@edu.uz", "Namangan viloyati, Chust tumani", "Namangan viloyati", "Chust", "+998901110007", 2, 1, 2, "To'lov-shartnoma", "Kunduzgi", "Bakalavr", 2, 2023, "O'qimoqda"),
            ("39523110008", "Ulug'bek", "Mahmudov", "Zokir o'g'li", "31912035600088", "AF3322119", "2004-12-19", "Erkak", "+998901230008", "ulugbek.m@edu.uz", "Xorazm viloyati, Urganch shahri", "Xorazm viloyati", "Urganch", "+998901110008", 2, 1, 2, "To'lov-shartnoma", "Kunduzgi", "Bakalavr", 2, 2023, "O'qimoqda"),
            ("39523110009", "Zilola", "Ismoilova", "Baxtiyor qizi", "41406035600099", "AG8877665", "2004-06-14", "Ayol", "+998901230009", "zilola.i@edu.uz", "Navoiy viloyati, Zarafshon shahri", "Navoiy viloyati", "Zarafshon", "+998901110009", 2, 1, 2, "Davlat granti", "Kunduzgi", "Bakalavr", 2, 2023, "O'qimoqda"),

            # Group 3: SI-24-01 (Faculty 1, Specialty 3, Course 1)
            ("39524110010", "Mirjalol", "Bekmurodov", "Erkin o'g'li", "30202045600010", "AH1238901", "2005-02-02", "Erkak", "+998901230010", "mirjalol.b@edu.uz", "Surxondaryo viloyati, Termiz shahri", "Surxondaryo viloyati", "Termiz", "+998901110010", 3, 1, 3, "To'lov-shartnoma", "Kunduzgi", "Bakalavr", 1, 2024, "O'qimoqda"),
            ("39524110011", "Rayhona", "Xudoyberdiyeva", "Ilhom qizi", "41905045600012", "AJ9012345", "2005-05-19", "Ayol", "+998901230011", "rayhona.x@edu.uz", "Toshkent viloyati, Chirchiq shahri", "Toshkent viloyati", "Chirchiq", "+998901110011", 3, 1, 3, "Davlat granti", "Kunduzgi", "Bakalavr", 1, 2024, "O'qimoqda"),
            ("39524110012", "Temur", "Rustamov", "Sanjar o'g'li", "32810045600013", "AK6789012", "2005-10-28", "Erkak", "+998901230012", "temur.r@edu.uz", "Jizzax viloyati, Zomin tumani", "Jizzax viloyati", "Zomin", "+998901110012", 3, 1, 3, "To'lov-shartnoma", "Kunduzgi", "Bakalavr", 1, 2024, "O'qimoqda"),

            # Group 4: IQ-22-03 (Faculty 2, Specialty 4, Course 3)
            ("39522110013", "Kamron", "G'aniyev", "Davron o'g'li", "31103025600014", "AL2345678", "2003-03-11", "Erkak", "+998901230013", "kamron.g@edu.uz", "Sirdaryo viloyati, Guliston shahri", "Sirdaryo viloyati", "Guliston", "+998901110013", 4, 2, 4, "Davlat granti", "Kunduzgi", "Bakalavr", 3, 2022, "O'qimoqda"),
            ("39522110014", "Gulbahor", "Norova", "Hamid qizi", "42207025600015", "AM3456789", "2003-07-22", "Ayol", "+998901230014", "gulbahor.n@edu.uz", "Samarqand viloyati, Kattaqo'rg'on shahri", "Samarqand viloyati", "Kattaqo'rg'on", "+998901110014", 4, 2, 4, "To'lov-shartnoma", "Kunduzgi", "Bakalavr", 3, 2022, "O'qimoqda"),
            ("39522110015", "Farrux", "Ibrohimov", "Mansur o'g'li", "30911025600016", "AN4567890", "2003-11-09", "Erkak", "+998901230015", "farrux.i@edu.uz", "Toshkent shahri, Yunusobod tumani", "Toshkent shahri", "Yunusobod", "+998901110015", 4, 2, 4, "To'lov-shartnoma", "Kunduzgi", "Bakalavr", 3, 2022, "O'qimoqda"),

            # Group 5: MF-23-01 (Faculty 2, Specialty 5, Course 2)
            ("39523110016", "Nodir", "Hasanov", "Sherzod o'g'li", "31401035600017", "AP5678901", "2004-01-14", "Erkak", "+998901230016", "nodir.h@edu.uz", "Buxoro shahri", "Buxoro viloyati", "Buxoro", "+998901110016", 5, 2, 5, "To'lov-shartnoma", "Kunduzgi", "Bakalavr", 2, 2023, "O'qimoqda"),
            ("39523110017", "Munisa", "Oripova", "Ravshan qizi", "41808035600018", "AR6789012", "2004-08-18", "Ayol", "+998901230017", "munisa.o@edu.uz", "Farg'ona shahri", "Farg'ona viloyati", "Farg'ona", "+998901110017", 5, 2, 5, "Davlat granti", "Kunduzgi", "Bakalavr", 2, 2023, "O'qimoqda"),

            # Group 6: BM-24-01 (Faculty 3, Specialty 6, Course 1)
            ("39524110018", "Doston", "Saidov", "Jamshid o'g'li", "32704045600019", "AS7890123", "2005-04-27", "Erkak", "+998901230018", "doston.s@edu.uz", "Qashqadaryo viloyati, Shahrisabz tumani", "Qashqadaryo viloyati", "Shahrisabz", "+998901110018", 6, 3, 6, "Davlat granti", "Kunduzgi", "Bakalavr", 1, 2024, "O'qimoqda"),
            ("39524110019", "Mohinur", "Aliyeva", "Kamol qizi", "40909045600020", "AT8901234", "2005-09-09", "Ayol", "+998901230019", "mohinur.a@edu.uz", "Toshkent shahri, Mirzo Ulug'bek tumani", "Toshkent shahri", "Mirzo Ulug'bek", "+998901110019", 6, 3, 6, "To'lov-shartnoma", "Kunduzgi", "Bakalavr", 1, 2024, "O'qimoqda"),

            # Group 7: DI-24-02 (Faculty 1, Specialty 1, Course 1, Kechki)
            ("39524110020", "Sherzod", "Yoqubov", "Vali o'g'li", "30303045600021", "AU9012345", "2001-03-03", "Erkak", "+998901230020", "sherzod.y@edu.uz", "Andijon shahri", "Andijon viloyati", "Andijon", "+998901110020", 7, 1, 1, "To'lov-shartnoma", "Kechki", "Bakalavr", 1, 2024, "O'qimoqda"),
            
            # Special Statuses: Academic Leave & Expelled
            ("39521110021", "Akrom", "Samadov", "Botir o'g'li", "31505015600022", "AV0123456", "2002-05-15", "Erkak", "+998901230021", "akrom.s@edu.uz", "Namangan viloyati", "Namangan viloyati", "Namangan", "+998901110021", 8, 1, 2, "To'lov-shartnoma", "Sirtqi", "Bakalavr", 4, 2021, "Akademik ta'til"),
            ("39521110022", "Bekzod", "Toirov", "Alisher o'g'li", "31606015600023", "AW1234567", "2002-06-16", "Erkak", "+998901230022", "bekzod.t@edu.uz", "Toshkent viloyati", "Toshkent viloyati", "Parkent", "+998901110022", 8, 1, 2, "To'lov-shartnoma", "Sirtqi", "Bakalavr", 4, 2021, "Chetlashtirilgan"),
        ]

        for s in uzbek_students:
            code, first, last, mid, pinfl, passp, bdate, gen, phone, email, addr, reg, dist, pphone, gid, fid, spid, pform, etype, edeg, clvl, ayear, stat = s
            fname = f"{last} {first} {mid}".strip()
            cursor.execute("""
                INSERT INTO students (
                    student_code, first_name, last_name, middle_name, full_name,
                    pinfl, passport_number, birth_date, gender, nationality,
                    phone, email, address, region, district, parent_phone,
                    group_id, faculty_id, specialty_id, payment_form,
                    education_type, education_degree, course_level, admission_year,
                    status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'O''zbek', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (code, first, last, mid, fname, pinfl, passp, bdate, gen, phone, email, addr, reg, dist, pphone, gid, fid, spid, pform, etype, edeg, clvl, ayear, stat))
            student_id = cursor.lastrowid

            # Create user account for student portal
            cursor.execute("""
                INSERT INTO users (username, password_hash, full_name, role, email, phone, student_id)
                VALUES (?, ?, ?, 'student', ?, ?, ?)
            """, (code.lower(), hash_password("student123"), fname, email, phone, student_id))

            # Contract if To'lov-shartnoma
            if pform == "To'lov-shartnoma":
                c_num = f"SH-{code[-5:]}/2025"
                total_amt = 12000000.0
                paid_amt = 12000000.0 if student_id % 3 == 0 else (6000000.0 if student_id % 2 == 0 else 0.0)
                c_status = "To'langan" if paid_amt >= total_amt else ("Qisman to'langan" if paid_amt > 0 else "Qarzdor")
                cursor.execute("""
                    INSERT INTO contracts (student_id, academic_year, contract_number, total_amount, paid_amount, status)
                    VALUES (?, '2025-2026', ?, ?, ?, ?)
                """, (student_id, c_num, total_amt, paid_amt, c_status))
                cid = cursor.lastrowid
                if paid_amt > 0:
                    cursor.execute("""
                        INSERT INTO payments (contract_id, student_id, amount, payment_date, payment_method, receipt_number)
                        VALUES (?, ?, ?, '2025-10-15', 'Bank o''tkazmasi', ?)
                    """, (cid, student_id, paid_amt, f"REC-{code[-5:]}"))

            # Assign some students to Dormitory
            if student_id in [1, 2, 6, 7, 10]:
                room_id = 1 if gen == "Erkak" else 3
                cursor.execute("""
                    INSERT INTO dormitory_residents (room_id, student_id, check_in_date, status)
                    VALUES (?, ?, '2024-09-01', 'Yashamoqda')
                """, (room_id, student_id))

        # 10. Timetables
        print("Dars jadvallari kiritilmoqda...")
        timetables = [
            # Group 1 (DI-22-01)
            (1, 1, 1, 1, 1, "402-xona", "Ma'ruza"), # Dushanba 1-juftlik
            (1, 2, 2, 1, 2, "305-xona", "Amaliy"),  # Dushanba 2-juftlik
            (1, 3, 3, 2, 1, "Komp-10", "Laboratoriya"), # Seshanba 1-juftlik
            (1, 12, 1, 3, 2, "Komp-12", "Amaliy"), # Chorshanba 2-juftlik
            (1, 4, 2, 4, 1, "501-xona", "Ma'ruza"), # Payshanba 1-juftlik
            
            # Group 2 (KI-23-02)
            (2, 2, 2, 1, 1, "305-xona", "Ma'ruza"),
            (2, 10, 2, 2, 2, "401-xona", "Amaliy"),
            (2, 6, 3, 3, 1, "Komp-08", "Laboratoriya"),
        ]
        cursor.executemany("""
            INSERT INTO timetables (group_id, subject_id, teacher_id, day_of_week, pair_number, room_number, lesson_type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, timetables)

        # 11. Grades
        print("Baholar va kredit-modul ko'rsatkichlari kiritilmoqda...")
        cursor.execute("SELECT id FROM students WHERE group_id = 1")
        g1_students = [r[0] for r in cursor.fetchall()]

        grades_seed = [
            (0, 1, 38.0, 18.0, 36.0), # 92.0 -> A
            (0, 2, 35.0, 17.0, 34.0), # 86.0 -> B+
            (0, 3, 37.0, 19.0, 37.0), # 93.0 -> A
            (0, 12, 36.0, 18.0, 35.0), # 89.0 -> B+

            (1, 1, 36.0, 17.0, 35.0), # 88.0 -> B+
            (1, 2, 34.0, 16.0, 32.0), # 82.0 -> B
            (1, 3, 39.0, 19.0, 38.0), # 96.0 -> A
            (1, 12, 37.0, 18.0, 36.0), # 91.0 -> A

            (2, 1, 30.0, 15.0, 28.0), # 73.0 -> C
            (2, 2, 28.0, 14.0, 26.0), # 68.0 -> D
            (2, 3, 32.0, 15.0, 30.0), # 77.0 -> C+
            (2, 12, 29.0, 13.0, 25.0), # 67.0 -> D

            (3, 1, 39.0, 20.0, 39.0), # 98.0 -> A
            (3, 2, 38.0, 19.0, 38.0), # 95.0 -> A
            (3, 3, 39.0, 19.0, 37.0), # 95.0 -> A
            (3, 12, 38.0, 18.0, 38.0), # 94.0 -> A

            (4, 1, 25.0, 10.0, 20.0), # 55.0 -> F (Qarzdor)
            (4, 2, 28.0, 12.0, 24.0), # 64.0 -> D
            (4, 3, 30.0, 14.0, 26.0), # 70.0 -> C
            (4, 12, 26.0, 11.0, 21.0), # 58.0 -> F (Qarzdor)
        ]

        for idx, sub_id, jn, on, yn in grades_seed:
            if idx < len(g1_students):
                st_id = g1_students[idx]
                tot = round(jn + on + yn, 1)
                l_grade, gp = calculate_letter_and_gpa(tot)
                stat = "O'tdi" if tot >= 60 else "Qarzdor"
                cursor.execute("""
                    INSERT INTO grades (
                        student_id, subject_id, semester, academic_year,
                        current_grade, midterm_grade, final_grade,
                        total_score, letter_grade, gpa_point, status, updated_at
                    ) VALUES (?, ?, 5, '2025-2026', ?, ?, ?, ?, ?, ?, ?, datetime('now', 'localtime'))
                """, (st_id, sub_id, jn, on, yn, tot, l_grade, gp, stat))

        # 12. Attendance records
        print("Davomat qaydnomalari kiritilmoqda...")
        dates = ["2025-11-03", "2025-11-04", "2025-11-05", "2025-11-06", "2025-11-07", "2025-11-10"]
        for st_id in g1_students:
            for d in dates:
                att_status = "Bor"
                if st_id == g1_students[4]:
                    att_status = "Sababsiz"
                elif st_id == g1_students[2] and d == "2025-11-05":
                    att_status = "Sababli"
                cursor.execute("""
                    INSERT INTO attendance (student_id, subject_id, group_id, date, pair_number, status, hours)
                    VALUES (?, 1, 1, ?, 1, ?, 2)
                """, (st_id, d, att_status))

        # For student 4, add extra unexcused absences so it triggers the >74 hours warning logic!
        st_4 = g1_students[4]
        for extra_day in range(1, 38):
            d_str = f"2025-10-{extra_day:02d}" if extra_day <= 31 else f"2025-09-{extra_day-31:02d}"
            cursor.execute("""
                INSERT INTO attendance (student_id, subject_id, group_id, date, pair_number, status, hours, notes)
                VALUES (?, 2, 1, ?, 2, 'Sababsiz', 2, 'Darsga sababsiz kelmadi')
            """, (st_4, d_str))

    print("Barcha demo ma'lumotlar muvaffaqiyatli kiritildi!")

if __name__ == "__main__":
    seed_database()
