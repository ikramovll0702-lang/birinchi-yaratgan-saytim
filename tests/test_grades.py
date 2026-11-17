import pytest
from app.services.grade_service import calculate_letter_and_gpa

def test_hemis_grade_letter_and_gpa_scale():
    # 90-100 -> A, 4.0
    letter, gpa = calculate_letter_and_gpa(95.0)
    assert letter == "A"
    assert gpa == 4.0

    letter, gpa = calculate_letter_and_gpa(90.0)
    assert letter == "A"
    assert gpa == 4.0

    # 85-89.9 -> B+, 3.5
    letter, gpa = calculate_letter_and_gpa(87.5)
    assert letter == "B+"
    assert gpa == 3.5

    # 80-84.9 -> B, 3.0
    letter, gpa = calculate_letter_and_gpa(81.0)
    assert letter == "B"
    assert gpa == 3.0

    # 75-79.9 -> C+, 2.5
    letter, gpa = calculate_letter_and_gpa(77.0)
    assert letter == "C+"
    assert gpa == 2.5

    # 70-74.9 -> C, 2.0
    letter, gpa = calculate_letter_and_gpa(71.0)
    assert letter == "C"
    assert gpa == 2.0

    # 60-69.9 -> D, 1.0
    letter, gpa = calculate_letter_and_gpa(63.0)
    assert letter == "D"
    assert gpa == 1.0

    # 0-59.9 -> F, 0.0 (Fail)
    letter, gpa = calculate_letter_and_gpa(58.0)
    assert letter == "F"
    assert gpa == 0.0

    letter, gpa = calculate_letter_and_gpa(0.0)
    assert letter == "F"
    assert gpa == 0.0

