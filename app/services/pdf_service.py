import io
import datetime
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm, mm
from reportlab.pdfgen import canvas
from app.services.grade_service import get_student_transcript, calculate_student_gpa

def generate_student_certificate_pdf(student: dict) -> io.BytesIO:
    """
    O'qish joyidan ma'lumotnoma (Official Student Certificate)
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    story = []
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        alignment=1, # Center
        spaceAfter=15,
        textColor=colors.HexColor('#1e3a8a')
    )
    header_org_style = ParagraphStyle(
        'OrgHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        alignment=1,
        spaceAfter=4,
        textColor=colors.HexColor('#0f172a')
    )
    sub_org_style = ParagraphStyle(
        'SubOrgHeader',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        alignment=1,
        spaceAfter=15,
        textColor=colors.HexColor('#475569')
    )
    body_style = ParagraphStyle(
        'CertBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=18,
        spaceAfter=12,
        textColor=colors.HexColor('#1f2937')
    )
    bold_body_style = ParagraphStyle(
        'CertBoldBody',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=18,
        textColor=colors.HexColor('#0f172a')
    )

    # University header
    story.append(Paragraph("O'ZBEKISTON RESPUBLIKASI OLIY TA'LIM, FAN VA INNOVATSIYALAR VAZIRLIGI", header_org_style))
    story.append(Paragraph("DAVLAT UNIVERSITETI TALABALARNI BOSHQARISH AXBOROT TIZIMI", header_org_style))
    story.append(Paragraph("Toshkent shahri, Universitet ko'chasi 4-uy | Tel: +998 (71) 200-00-00 | Web: www.edu.uz", sub_org_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1e3a8a'), spaceAfter=20))

    now = datetime.datetime.now()
    doc_num = f"ML-{student['id']:04d}/{now.year}"
    date_str = now.strftime("%d.%m.%Y")

    # Meta date and number
    meta_table = Table([
        [Paragraph(f"<b>Hujjat raqami:</b> {doc_num}", body_style),
         Paragraph(f"<b>Berilgan sana:</b> {date_str}", ParagraphStyle('RightMeta', parent=body_style, alignment=2))]
    ], colWidths=[260, 260])
    story.append(meta_table)
    story.append(Spacer(1, 20))

    story.append(Paragraph("MA'LUMOTNOMA", title_style))
    story.append(Spacer(1, 10))

    # Text content
    text = (
        f"Ushbu ma'lumotnoma berildiki fuqaro <b>{student['full_name']}</b>ga (JSHSHIR: {student.get('pinfl') or 'Mavjud emas'}, "
        f"Pasport: {student.get('passport_number') or 'Mavjud emas'}), u haqiqatdan ham Davlat Universiteti "
        f"<b>{student['faculty_name']}</b> fakulteti <b>{student['specialty_name']}</b> yo'nalishi "
        f"<b>{student['group_name']}</b>-guruh <b>{student['course_level']}</b>-bosqich talabasi ekanligi tasdiqlanadi.<br/><br/>"
        f"<b>Ta'lim turi:</b> {student['education_degree']}<br/>"
        f"<b>Ta'lim shakli:</b> {student['education_type']}<br/>"
        f"<b>To'lov shakli:</b> {student['payment_form']}<br/>"
        f"<b>Talabalik ID raqami:</b> {student['student_code']}<br/>"
        f"<b>O'qishga qabul qilingan yili:</b> {student['admission_year']}-yil<br/>"
        f"<b>Hozirgi holati:</b> {student['status']}<br/><br/>"
        f"Ma'lumotnoma talab qilingan joyga taqdim etish uchun berildi. Ushbu hujjat universitetning axborot tizimi orqali "
        f"elektron tarzda shakllantirilgan bo'lib, davlat yagona HEMIS tizimi talablariga to'liq javob beradi."
    )
    story.append(Paragraph(text, body_style))
    story.append(Spacer(1, 30))

    # Signatures & Official stamp box
    sig_data = [
        [
            Paragraph(f"<b>Fakultet dekani:</b> {student.get('dean_name') or 'Prof. A. Xoliqov'}<br/><i>(Imzo va muhr)</i>", body_style),
            Paragraph(
                f"<font color='#059669'><b>[ ELEKTRON TASDIQLANGAN ]</b></font><br/>"
                f"<font size=8 color='#4b5563'>Tizim tekshiruv kodi: HEMIS-VERIF-{student['id']:05d}<br/>"
                f"Tekshirish manzili: hemis.edu.uz/verify/{doc_num}</font>",
                ParagraphStyle('QRStyle', parent=body_style, alignment=2)
            )
        ]
    ]
    sig_table = Table(sig_data, colWidths=[260, 260])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(sig_table)

    doc.build(story)
    buffer.seek(0)
    return buffer

def generate_transcript_pdf(student: dict) -> io.BytesIO:
    """
    Talabaning akademik transkripti (HEMIS Reyting daftarchasi)
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=35,
        bottomMargin=35
    )
    story = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=14,
        alignment=1,
        spaceAfter=10,
        textColor=colors.HexColor('#1e3a8a')
    )
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        alignment=1,
        spaceAfter=3,
        textColor=colors.HexColor('#0f172a')
    )
    cell_style = ParagraphStyle(
        'Cell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11
    )
    cell_bold = ParagraphStyle(
        'CellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11
    )

    story.append(Paragraph("DAVLAT UNIVERSITETI", header_style))
    story.append(Paragraph("AKADEMIK TRANSKRIPT / REYTING DAFTARCHASI", title_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceAfter=15))

    # Student Info Grid
    gpa = calculate_student_gpa(student["id"])
    info_data = [
        [Paragraph(f"<b>Talaba:</b> {student['full_name']}", cell_style),
         Paragraph(f"<b>Talaba ID:</b> {student['student_code']}", cell_style)],
        [Paragraph(f"<b>Fakultet:</b> {student['faculty_name']}", cell_style),
         Paragraph(f"<b>Guruh:</b> {student['group_name']}", cell_style)],
        [Paragraph(f"<b>Yo'nalish:</b> {student['specialty_name']}", cell_style),
         Paragraph(f"<b>Kurs:</b> {student['course_level']}-bosqich", cell_style)],
        [Paragraph(f"<b>Ta'lim turi/shakli:</b> {student['education_degree']} / {student['education_type']}", cell_style),
         Paragraph(f"<b>Umumiy GPA:</b> <font color='#16a34a' size=10><b>{gpa:.2f}</b></font>", cell_style)]
    ]
    info_table = Table(info_data, colWidths=[270, 270])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#e2e8f0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 15))

    # Transcript grades table
    grades = get_student_transcript(student["id"])
    table_rows = [
        [
            Paragraph("№", cell_bold),
            Paragraph("Fan kodi va nomi", cell_bold),
            Paragraph("Semestr", cell_bold),
            Paragraph("Kredit", cell_bold),
            Paragraph("JN (40)", cell_bold),
            Paragraph("ON (20)", cell_bold),
            Paragraph("YN (40)", cell_bold),
            Paragraph("Jami (100)", cell_bold),
            Paragraph("Baho", cell_bold),
            Paragraph("GPA", cell_bold),
        ]
    ]

    total_credits = 0
    for idx, g in enumerate(grades, 1):
        total_credits += g["credits"]
        table_rows.append([
            Paragraph(str(idx), cell_style),
            Paragraph(f"<b>{g['subject_code']}</b> - {g['subject_name']}", cell_style),
            Paragraph(str(g['semester']), cell_style),
            Paragraph(str(g['credits']), cell_style),
            Paragraph(str(g['current_grade']), cell_style),
            Paragraph(str(g['midterm_grade']), cell_style),
            Paragraph(str(g['final_grade']), cell_style),
            Paragraph(f"<b>{g['total_score']}</b>", cell_style),
            Paragraph(f"<b>{g['letter_grade']}</b>", cell_style),
            Paragraph(str(g['gpa_point']), cell_style),
        ])

    if not grades:
        table_rows.append([Paragraph("Hozircha baholar kiritilmagan", cell_style)] + [Paragraph("", cell_style)] * 9)

    t_table = Table(table_rows, colWidths=[22, 190, 45, 38, 40, 40, 40, 45, 38, 42])
    t_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')])
    ]))
    story.append(t_table)
    story.append(Spacer(1, 20))

    # Summary
    summary_text = (
        f"<b>O'zlashtirilgan umumiy kreditlar soni:</b> {total_credits} ECTS<br/>"
        f"<b>Kredit-modul tizimi bo'yicha yakuniy GPA ko'rsatkichi:</b> {gpa:.2f} / 4.00"
    )
    story.append(Paragraph(summary_text, cell_style))
    story.append(Spacer(1, 25))

    # Signature
    sig_table = Table([
        [
            Paragraph("<b>O'quv ishlari bo'yicha prorektor:</b> ________________", cell_style),
            Paragraph("<b>Fakultet dekani:</b> ________________", cell_style),
        ]
    ], colWidths=[270, 270])
    story.append(sig_table)

    doc.build(story)
    buffer.seek(0)
    return buffer

def generate_student_id_card_pdf(student: dict) -> io.BytesIO:
    """
    Talabalik guvohnomasi (Student ID Card)
    """
    buffer = io.BytesIO()
    # ID card dimensions roughly 85mm x 54mm (Credit Card size), or half-A4 page
    doc = SimpleDocTemplate(
        buffer,
        pagesize=(85.6 * mm, 54 * mm),
        rightMargin=3 * mm,
        leftMargin=3 * mm,
        topMargin=3 * mm,
        bottomMargin=3 * mm
    )
    story = []
    styles = getSampleStyleSheet()

    header_style = ParagraphStyle(
        'CardHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.5,
        alignment=1,
        textColor=colors.white
    )
    sub_header = ParagraphStyle(
        'CardSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=5.5,
        alignment=1,
        textColor=colors.HexColor('#e2e8f0')
    )
    name_style = ParagraphStyle(
        'CardName',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7,
        leading=8,
        textColor=colors.HexColor('#0f172a')
    )
    item_style = ParagraphStyle(
        'CardItem',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=5.5,
        leading=7,
        textColor=colors.HexColor('#334155')
    )

    # Header bar
    header_data = [[
        Paragraph("<b>O'ZBEKISTON RESPUBLIKASI DAVLAT UNIVERSITETI</b>", header_style),
    ], [
        Paragraph("TALABALIK GUVOHNOMASI / STUDENT ID", sub_header)
    ]]
    h_table = Table(header_data, colWidths=[79 * mm])
    h_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1e3a8a')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(h_table)
    story.append(Spacer(1, 2 * mm))

    # Photo placeholder and Info
    photo_box = Paragraph(
        f"<font size=5 color='#64748b'>[ RASM ]<br/>3x4</font>",
        ParagraphStyle('Photo', alignment=1)
    )

    info_content = [
        Paragraph(f"<b>{student['full_name']}</b>", name_style),
        Paragraph(f"<b>ID:</b> {student['student_code']}", item_style),
        Paragraph(f"<b>Fakultet:</b> {student['faculty_name'][:25]}...", item_style),
        Paragraph(f"<b>Guruh:</b> {student['group_name']} | Kurs: {student['course_level']}", item_style),
        Paragraph(f"<b>Amal qilish muddati:</b> 2024 - 2028", item_style),
    ]

    body_table = Table([
        [photo_box, info_content]
    ], colWidths=[20 * mm, 59 * mm])
    body_table.setStyle(TableStyle([
        ('BOX', (0,0), (0,0), 0.5, colors.HexColor('#94a3b8')),
        ('BACKGROUND', (0,0), (0,0), colors.HexColor('#f1f5f9')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('LEFTPADDING', (1,0), (1,0), 3 * mm),
    ]))
    story.append(body_table)

    doc.build(story)
    buffer.seek(0)
    return buffer

