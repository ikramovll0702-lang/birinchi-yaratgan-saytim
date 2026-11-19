# HEMIS - Oliy Ta'lim Muassasasi Talabalarini Boshqarish Axborot Tizimi

Oliy ta'lim muassasalari (OTM) uchun talabalar haqidagi ma'lumotlarni to'liq raqamlashtirish, kredit-modul tizimi (ECTS) asosida o'quv jarayonini boshqarish, baholar va davomatni yuritish, shartnoma to'lovlari hamda talabalar turar joyi hisobini olib borish uchun mo'ljallangan zamonaviy, to'liq funksional veb tizim.

---

## 🚀 Tizimning Asosiy Imkoniyatlari

### 1. 📊 Boshqaruv Paneli (Dashboard & Analitika)
- **Asosiy ko'rsatkichlar (KPI):** Jami talabalar soni, faol o'qiyotganlar, akademik ta'tildagilar, chetlashtirilganlar, fakultetlar, kafedralar, guruhlar soni.
- **Interaktiv grafiklar (Chart.js):**
  - Fakultetlar kesimida talabalar taqsimoti (Ustunli diagramma).
  - Kurslar bo'yicha taqsimot (1-kursdan 4-kursgacha halqasimon diagramma).
  - To'lov shakli nisbati: Davlat granti va To'lov-shartnoma (Doiraviy diagramma).
  - Universitet bo'yicha o'rtacha GPA ko'rsatkichi.
- **74+ soat ogohlantirish signallari:** Sababsiz dars qoldirgan talabalar bo'yicha tezkor ogohlantirish.
- **So'nggi harakatlar va yangi talabalar ro'yxati.**

### 2. 🎓 Talabalar Boshqaruvi (Student 360° Management)
- **To'liq CRUD:** Yangi talaba qo'shish, ma'lumotlarni tahrirlash, o'chirish.
- **Avtomatlashtirilgan Talaba ID:** HEMIS standarti bo'yicha noyob 11 xonali talaba identifikatori (masalan: `39524110001`).
- **360-gradus Talaba Profili:**
  - Shaxsiy ma'lumotlar: F.I.Sh., JSHSHIR (PINFL 14 xonali), Pasport seriya/raqam, tug'ilgan sana, jinsi, telefon, email, manzil, viloyat/tuman, ota-onasining telefoni.
  - O'quv ma'lumotlari: Fakultet, Yo'nalish, Guruh, Ta'lim shakli (Kunduzgi, Kechki, Sirtqi), Ta'lim turi (Bakalavr, Magistr), To'lov shakli (Grant / Shartnoma), Qabul yili, Holati.
  - O'zlashtirish va kredit-modul ko'rsatkichlari (Semestrlar bo'yicha fanlar, nazorat ballari, harfli baho, GPA).
  - Davomat monitoringi (Qoldirilgan soatlar, sababli/sababsiz).
  - To'lov-shartnoma balansi, kvitansiyalar tarixi.
  - Talabalar turar joyi (TTJ / Yotoqxona) ma'lumoti.
- **Ko'p parametrli filtrlash:** F.I.Sh., Talaba ID, JSHSHIR, Fakultet, Yo'nalish, Guruh, Kurs, To'lov turi, Holat, Jins bo'yicha.

### 3. 📄 Hujjatlar va Hisobotlar Generatsiyasi (PDF & Excel)
- **O'qish joyidan ma'lumotnoma (PDF):** Davlat standarti bo'yicha rasmiy gerbli blanka, elektron tasdiqlash kodi, dekanat muhri va QR tekshiruv havolasi bilan.
- **Akademik transkript / Reyting daftarchasi (PDF):** Fanlar kodi, ECTS kreditlari, JN, ON, YN ballari, 100 ballik tizimdagi natija, harfli baholar va GPA hisobi.
- **Talabalik guvohnomasi (Student ID Card PDF):** 3x4 rasm joyi, shtrix-kod, talaba ID va amal qilish muddati bilan zamonaviy guvohnoma formati.
- **Excelga eksport:** Barcha yoki filtrlangan talabalar ro'yxatini to'liq formatlangan `.xlsx` fayl ko'rinishida yuklab olish.
- **Excel orqali ommaviy import:** Maxsus tayyorlangan namunaviy shablon yordamida yuzlab talabalarni bir zumda bazaga kiritish.

### 4. 🏛️ Fakultet, Kafedra, Yo'nalish va Guruhlar
- Fakultetlar strukturasi, dekanlar, kafedralar va yo'nalishlar boshqaruvi.
- Akademik guruhlar ro'yxati, kursi, ta'lim shakli, tili va biriktirilgan tyutor/murabbiy.
- Dinamik (kaskad) tanlov: Fakultet tanlanganda yo'nalish va guruhlar avtomatik yangilanadi.

### 5. 📚 O'quv Jarayoni va Dars Jadvali
- O'quv rejasidagi fanlar (kodi, nomi, semestri, ECTS kreditlari, ma'ruza, amaliy, laboratoriya va mustaqil ta'lim soatlari).
- Professor-o'qituvchilar bazasi (ilmiy darajalari, lavozimi, aloqa ma'lumotlari).
- Haftalik dars jadvali (1-kun Dushanbadan 6-kun Shanbagacha, 1-4 juftliklar, xonalar va dars turlari).

### 6. 🏆 Kredit-Modul Baholash Tizimi (ECTS & GPA)
- O'zbekiston Respublikasi OTM me'yoriy Nizomiga to'liq mos keladigan baholash shkalasi:
  - **90 – 100 ball:** `A` (GPA: 4.0) — A'lo
  - **85 – 89 ball:** `B+` (GPA: 3.5) — Yaxshi
  - **80 – 84 ball:** `B` (GPA: 3.0) — Yaxshi
  - **75 – 79 ball:** `C+` (GPA: 2.5) — Qoniqarli
  - **70 – 74 ball:** `C` (GPA: 2.0) — Qoniqarli
  - **60 – 69 ball:** `D` (GPA: 1.0) — Qoniqarli
  - **0 – 59 ball:** `F` (GPA: 0.0) — Qoniqarsiz (Akademik qarzdor)
- Nazorat turlari: Joriy nazorat (max 40), Oraliq nazorat (max 20), Yakuniy nazorat (max 40).
- Jami ball, harfli baho va GPA ballining avtomatik real vaqtda qayta hisoblanishi.
- HEMIS GPA formulasi: $$\text{GPA} = \frac{\sum (\text{Kredit} \times \text{GPA\_Ball})}{\sum \text{Kredit}}$$

### 7. ⏱️ Davomat Tizimi va 74+ Soatlik Nazorat
- Guruhlar va fanlar kesimida kunlik elektron davomat qaydnomasi.
- Holatlar: **Bor**, **Sababli**, **Sababsiz**.
- "Barchasi bor" bitta tugma bilan belgilash.
- **HEMIS qoidasi:** Semestr davomida sababsiz 74 soatdan ortiq dars qoldirgan talabalarni avtomatik aniqlash va intizomiy chora ko'rish bo'limi.

### 8. 💳 To'lov-Shartnomalar va Moliya
- To'lov-shartnoma asosida tahsil olayotgan talabalar uchun avtomatik shartnoma generatsiyasi.
- Shartnoma summasi, to'langan mablag', qoldiq qarzdorlik hisobi.
- To'lov kvitansiyalarini qayd etish (Bank o'tkazmasi, Payme, Click, Uzum, Naqd).
- Qarzdor talabalar monitoringi.

### 9. 🏢 Talabalar Turar Joyi (TTJ / Yotoqxona)
- Yotoqxona binolari, qavatlari, xonalari, sig'imi va oylik ijara narxi.
- Talabalarni xonalarga joylashtirish (check-in) va xonadan chiqarish (check-out).
- Band va bo'sh o'rinlar hisobi.

### 10. 👤 Talaba Shaxsiy Kabineti (Student Portal)
- Talaba o'zining Talaba ID si va paroli orqali shaxsiy kabinetiga kiradi:
  - O'zlashtirish ko'rsatkichlari, fanlar bo'yicha ballari va GPA.
  - Davomat statistikasi va qoldirilgan soatlar monitoringi.
  - Haftalik dars jadvali va xonalar.
  - To'lov-shartnoma holati.
  - Bitta tugma bilan "O'qish joyidan ma'lumotnoma", "Reyting daftarchasi (Transkript)" va "Talabalik guvohnomasi" PDF hujjatlarini yuklab olish.

---

## ☁️ Railway.app Hostingga Joylashtirish (Deploy)

Loyiha Railway platformasida 100% avtomatik ishga tushish uchun to'liq moslashtirildi (`Procfile`, `railway.json`, `nixpacks.toml`, `Dockerfile`, `PORT` dinamik port bog'lanishi).

### 1-qadam: Railway'ga ulanish
1. [railway.app](https://railway.app/) saytiga kiring va GitHub hisobingiz bilan kiring (Login with GitHub).
2. **"+ New Project"** tugmasini bosing.
3. **"Deploy from GitHub repo"** ni tanlang.
4. Repozitoriyangizni tanlang: **`ikramovll0702-lang/birinchi-yaratgan-saytim`**.

### 2-qadam: Deploy
Railway avtomatik tarzda repozitoriydagi `railway.json` va `Procfile` ni taniydi va Python muhitini o'rnatib, ilovani ishga tushiradi. Hech qanday qo'shimcha buyruq yozish shart emas!

### 3-qadam: Domen olish (Public URL)
1. Railway loyiha panelida servisingiz ustiga bosing.
2. **"Settings"** bo'limiga o'ting.
3. **"Networking"** -> **"Generate Domain"** tugmasini bosing.
4. Sizga `https://birinchi-yaratgan-saytim-production.up.railway.app` kabi ommaviy bepul HTTPS domen beriladi!

### 4-qadam (Ixtiyoriy): Persistent Volume (Ma'lumotlar bazasi saqlanishi)
Agar konteyner qayta ishga tushganda ham kiritilgan talabalar va baholar o'chib ketmasligini xohlasangiz:
1. Railway servisining **"Volumes"** bo'limiga o'ting -> **"Add Volume"** bosing.
2. Mount path ga `/data` deb yozing.
3. **"Variables"** bo'limiga o'tib, quyidagi o'zgaruvchini qo'shing:
   - `DB_PATH` = `/data/university.db`

### Muhit o'zgaruvchilari (Environment Variables):
| O'zgaruvchi | Standart qiymat | Tavsif |
|---|---|---|
| `PORT` | `8000` | Railway avtomatik o'rnatadi |
| `HOST` | `0.0.0.0` | Barcha tarmoq interfeyslarida tinglash |
| `SECRET_KEY` | `hemis_secure_session_key_uz_2026_super_secret` | Sessiya cookie larini shifrlash kaliti |
| `DB_PATH` | `./university.db` | SQLite ma'lumotlar bazasi fayli joylashuvi |

---

## 🔑 Tizimga Kirish Uchun Demo Hisoblar

| Rol | Login | Parol | Huquqlari |
|---|---|---|---|
| **Administrator** | `admin` | `admin123` | Barcha amallar, fakultetlar, guruhlar, talabalar, o'chirish |
| **Dekanat** | `dekan` | `dekan123` | Talabalar, baholash jurnali, davomat, ma'lumotnomalar |
| **O'qituvchi** | `teacher` | `teacher123` | Baholash, davomat belgilash, dars jadvali |
| **Talaba Kabineti** | `39522110001` | `student123` | Shaxsiy baholar, GPA, davomat, ma'lumotnoma yuklab olish |

*(Login sahifasida bitta tugma orqali demo hisoblarni avtomatik to'ldirish imkoniyati mavjud)*

---

## 💻 Mahalliy Kompyuterda Ishga Tushirish

### 1. Talablarni o'rnatish:
```bash
python -m pip install -r requirements.txt
```

### 2. Tizimni ishga tushirish:
```bash
python run.py
```

Brauzerda quyidagi manzilni oching:
👉 **http://127.0.0.1:8000**

Swagger API interaktiv hujjatlari:
👉 **http://127.0.0.1:8000/docs**

---

## 📱 & 🖥️ Ilova Sifatida Ishlatish (PWA va Desktop Ilova)

Loyiha ham mobil qurilmalar (Android, iOS), ham shaxsiy kompyuterlar (Windows, macOS) uchun mustaqil ilova ko'rinishida foydalanishga to'liq moslashtirilgan:

### 1. 🖥️ Windows Desktop Dasturi (Mahalliy kompyuterda)
Tizimni brauzer ochmasdan, alohida mustaqil Windows dasturi (desktop ilova) sifatida ishlatishingiz mumkin:
- **Tezkor ishga tushirish:** `HEMIS-Ilova.bat` faylini ikki marta bosing.
- **Yoki terminaldan:**
  ```bash
  python desktop_app.py
  ```
Dastur orqa fonda serverni ishga tushiradi va zamonaviy **Microsoft Edge Chromium WebView2** motorida alohida chiroyli dastur oynasini ochadi.

### 2. 📱 Mobil va Desktop PWA (Progressive Web App)
Sayt ommaviy hostingga (masalan, Railway) yuklanganda yoki lokal ishlatilganda, uni telefon va kompyuterga to'liq ilova qilib o'rnatish mumkin:
- **Kompyuterda (Chrome, Edge):** Sayt ochilganda yuqori paneldagi **"Ilovani o'rnatish"** tugmasini bosing yoki brauzer manzil satridagi o'rnatish ikonkasini bosing.
- **Telefonda (Android / iOS):**
  - Android (Chrome): Saytga kirganda pastda "HEMIS ilovasini o'rnatish" taklifi chiqadi yoki brauzer menyusidan **"Ilovani o'rnatish" (Install app)** tanlanadi.
  - iPhone (Safari): **"Ulashish" (Share)** tugmasi -> **"Bosh ekranga qo'shish" (Add to Home Screen)** tanlanadi.
- **Afzalliklari:** Ilova telefonda va kompyuterda alohida belgi (ikonka) bilan paydo bo'ladi, brauzer qidiruv satrisiz to'liq ekranli ilova sifatida ishlaydi, kesh orqali tez yuklanadi.

---

## 🧪 Avtomatlashtirilgan Testlar Natijasi

Tizim barcha modullarni (Autentifikatsiya, Talabalar CRUD, HEMIS GPA formulasi, Davomat, Moliya, PDF va Excel generatsiyasi, PWA servis worker va manifest, HTTP API lar) qamrab oluvchi 28 ta avtomatlashtirilgan test bilan ta'minlangan.

Testlarni ishga tushirish:
```bash
python -m pytest tests -v
```

---

## 📁 Loyiha Tuzilmasi

```
maddikor/
├── app/
│   ├── main.py                  # Asosiy FastAPI ilovasi va marshrutlar
│   ├── database.py              # SQLite ulanishi, jadvallar va indekslar (DB_PATH moslashuvchan)
│   ├── auth.py                  # Xavfsiz PBKDF2 parollash, sessiyalar
│   ├── models.py                # Pydantic ma'lumot modellari
│   ├── templates_helper.py      # Shablon render qilish yordamchisi
│   ├── seed_data_auto.py        # Avtomatik dastlabki ma'lumotlarni kiritish
│   ├── services/
│   │   ├── student_service.py   # Talabalar boshqaruvi va filtrlash
│   │   ├── academic_service.py  # Fakultet, kafedra, guruh, fanlar
│   │   ├── grade_service.py     # HEMIS GPA va baholash formulalari
│   │   ├── attendance_service.py# Davomat va 74+ soat ogohlantirishlar
│   │   ├── finance_service.py   # Shartnomalar va to'lovlar
│   │   ├── pdf_service.py       # PDF Ma'lumotnoma, Transkript, ID Card
│   │   └── excel_service.py     # Excel eksport va import
│   ├── routers/
│   │   ├── auth_router.py       # Kirish, chiqish, profil
│   │   ├── dashboard_router.py  # Asosiy boshqaruv paneli
│   │   ├── students_router.py   # Talabalar bo'limi
│   │   ├── faculties_router.py  # Fakultetlar va guruhlar
│   │   ├── academics_router.py  # Fanlar va dars jadvali
│   │   ├── grades_router.py     # Kredit-modul jurnali
│   │   ├── attendance_router.py # Davomat va 74+ soat monitoring
│   │   ├── finance_router.py    # Shartnomalar va moliya
│   │   ├── dormitory_router.py  # Yotoqxona (TTJ)
│   │   ├── student_portal_router.py # Talaba shaxsiy kabineti
│   │   └── api_router.py        # Kaskad dropdown va qidiruv API lari
│   ├── static/
│   │   ├── css/custom.css       # Maxsus stillar
│   │   └── js/app.js            # Toast xabarlar, modal yordamchilari
│   └── templates/               # Jinja2 HTML shablonlari
├── tests/                       # Pytest testlar to'plami (25 ta test)
├── Procfile                     # Railway / Heroku ishga tushirish fayli
├── railway.json                 # Railway platformasi konfiguratsiyasi
├── nixpacks.toml                # Railway Nixpacks builder konfiguratsiyasi
├── Dockerfile                   # Docker konteyner fayli
├── .dockerignore                # Docker e'tiborsiz qoldiradigan fayllar
├── runtime.txt                  # Python versiyasi
├── seed_data.py                 # Namunaviy OTM ma'lumotlari generatori
├── run.py                       # Bir bosishda ishga tushirish skripti (HOST va PORT dinamik)
├── requirements.txt             # Kerakli kutubxonalar ro'yxati (gunicorn qo'shilgan)
└── README.md                    # Loyiha hujjatlari va Railway yo'riqnomasi
```
