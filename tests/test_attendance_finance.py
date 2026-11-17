import pytest
from app.services.attendance_service import mark_attendance, get_attendance_warnings
from app.services.finance_service import get_contracts, record_payment, get_finance_overview

def test_attendance_warnings():
    # In seed data, student 5 was given > 74 unexcused hours
    warnings = get_attendance_warnings(threshold_hours=74)
    assert isinstance(warnings, list)
    assert len(warnings) > 0
    first_warn = warnings[0]
    assert first_warn["unexcused_hours"] >= 74

def test_finance_overview():
    overview = get_finance_overview()
    assert overview["total_contracts"] > 0
    assert overview["total_expected"] > 0
    assert overview["total_received"] >= 0
    assert "total_debt" in overview

def test_contracts_list():
    contracts = get_contracts()
    assert len(contracts) > 0
    c = contracts[0]
    assert "contract_number" in c
    assert "student_name" in c
    assert "remaining_amount" in c

