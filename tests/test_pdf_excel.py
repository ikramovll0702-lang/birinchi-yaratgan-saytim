import pytest
from app.services.student_service import get_student_by_id, get_students
from app.services.pdf_service import (
    generate_student_certificate_pdf, generate_transcript_pdf, generate_student_id_card_pdf
)
from app.services.excel_service import (
    export_students_to_excel, generate_sample_import_template, import_students_from_excel
)

def test_pdf_generation():
    st = get_student_by_id(1)
    assert st is not None

    cert = generate_student_certificate_pdf(st)
    assert cert is not None
    cert_bytes = cert.getvalue()
    assert cert_bytes.startswith(b"%PDF")
    assert len(cert_bytes) > 1000

    trans = generate_transcript_pdf(st)
    assert trans is not None
    trans_bytes = trans.getvalue()
    assert trans_bytes.startswith(b"%PDF")
    assert len(trans_bytes) > 1000

    idc = generate_student_id_card_pdf(st)
    assert idc is not None
    idc_bytes = idc.getvalue()
    assert idc_bytes.startswith(b"%PDF")
    assert len(idc_bytes) > 500

def test_excel_export_and_template():
    students, _ = get_students(limit=5)
    xlsx = export_students_to_excel(students)
    assert xlsx is not None
    assert len(xlsx.getvalue()) > 1000

    tmpl = generate_sample_import_template()
    assert tmpl is not None
    assert len(tmpl.getvalue()) > 1000

def test_excel_import():
    # Import using the sample template itself!
    tmpl = generate_sample_import_template()
    result = import_students_from_excel(tmpl.getvalue())
    assert result["success"] is True
    assert result["count"] >= 1

