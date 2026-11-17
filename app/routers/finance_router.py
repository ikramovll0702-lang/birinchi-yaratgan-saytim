from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
import datetime
from typing import Optional
from app.templates_helper import render
from app.auth import get_current_user, require_roles, log_activity
from app.services.finance_service import (
    get_contracts, record_payment, get_finance_overview
)

router = APIRouter(prefix="/finance", tags=["finance"])

@router.get("", response_class=HTMLResponse)
async def finance_page(
    request: Request,
    status: Optional[str] = None,
    search: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    contracts = get_contracts(status=status, search=search)
    overview = get_finance_overview()
    current_date_iso = datetime.datetime.now().strftime("%Y-%m-%d")

    return render(request, "finance/contracts.html", {
        "current_user": current_user,
        "contracts": contracts,
        "overview": overview,
        "status": status,
        "search": search,
        "current_date_iso": current_date_iso
    })

@router.post("/payment")
async def record_payment_action(
    contract_id: int = Form(...),
    student_id: int = Form(...),
    amount: float = Form(...),
    payment_date: str = Form(...),
    payment_method: str = Form("Bank o'tkazmasi"),
    receipt_number: str = Form(""),
    notes: str = Form(""),
    current_user: dict = Depends(require_roles("admin", "dean"))
):
    record_payment(
        contract_id=contract_id,
        student_id=student_id,
        amount=amount,
        payment_date=payment_date,
        payment_method=payment_method,
        receipt_number=receipt_number,
        notes=notes
    )
    log_activity(current_user["id"], current_user["full_name"], "PAYMENT_RECORD", f"To'lov qabul qilindi: Student={student_id}, Summa={amount}")
    return RedirectResponse(url="/finance", status_code=status.HTTP_302_FOUND)
