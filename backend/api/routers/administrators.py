from fastapi import APIRouter, HTTPException
from api.schemas.payments import PaymentRequest, PaymentResponse, PaymentStatus
from api.utils import *
import uuid
import time

# Router for administrators
router = APIRouter()

# FastAPI endpoint to process ACH Debit payments for administrators
@router.post("/process-ach-debit", response_model=PaymentResponse)
async def process_ach_debit(payment: PaymentRequest):
    """Endpoint to process an ACH Debit payment for administrators"""
    try:
        result = perform_ach_debit(
            payment.internal_account_id,
            payment.external_account_id,
            payment.amount,
            payment.idempotency_key
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

