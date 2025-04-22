from fastapi import APIRouter, HTTPException
from api.schemas.payments import PaymentRequest, PaymentResponse, PaymentStatus
from api.utils import *
import uuid
import time

# Router for employees
router = APIRouter()


# FastAPI endpoint to process ACH Credit payments for employees
@router.post("/process-ach-credit", response_model=PaymentResponse)
async def process_ach_credit(payment: PaymentRequest):
    """Endpoint to process an ACH Credit payment for employees"""
    try:
        result = perform_ach_credit(
            payment.internal_account_id,
            payment.external_account_id,
            payment.amount,
            payment.idempotency_key
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
