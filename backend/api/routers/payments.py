from fastapi import APIRouter, HTTPException
from api.schemas.payments import PaymentRequest, PaymentResponse, PaymentStatus
from unittest.mock import patch
from random import randint
from api.utils import *
import uuid
import time

###################################### YOU CAN IGNORE THESE ##############################

# Router for payments
router = APIRouter()

# FastAPI endpoint to process ACH Debit payments
@router.post("/process-ach-debit", response_model=PaymentResponse)
async def process_ach_debit(payment: PaymentRequest):
    """Endpoint to process an ACH Debit payment"""
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


# FastAPI endpoint to process ACH Credit payments
@router.post("/process-ach-credit", response_model=PaymentResponse)
async def process_ach_credit(payment: PaymentRequest):
    """Endpoint to process an ACH Credit payment"""
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


# FastAPI endpoint to process Debit Card Swipe payments
@router.post("/process-swipe", response_model=PaymentResponse)
async def process_swipe(payment: PaymentRequest):
    """Endpoint to process a debit card swipe payment"""
    try:
        result = perform_swipe(
            payment.internal_account_id,  # Not used here, but included for consistency
            payment.amount,
            payment.idempotency_key
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint to get payment status (mocked)
@router.get("/payment-status/{payment_id}", response_model=PaymentStatus)
async def get_payment_status(payment_id: uuid.UUID):
    """Endpoint to check the status of a payment"""
    long_external_call()  # Simulating a long call to an external service
    return PaymentStatus.SUCCESS if randint(1, 2) == 1 else PaymentStatus.FAILURE


############## PATCH/UNIT TESTS #################

@patch("api.utils.external_call")
def test_perform_ach_debit(mock_external_call):
    mock_external_call.return_value = PaymentResponse(
        payment_id=uuid.uuid4(),
        status=PaymentStatus.PENDING,
        amount=5000,
    )
    response=perform_ach_debit(
        "internal_account_id",
        "external_account_id",
        5000,
        "idempotency_key",
    )
    assert response.status == PaymentStatus.PENDING
    

@patch("api.utils.external_call")
def test_perform_ach_credit(mock_external_call):
    mock_external_call.return_value = PaymentResponse(
        payment_id=uuid.uuid4(),
        status=PaymentStatus.PENDING,
        amount=5000,
    )
    response=perform_ach_credit(
        "internal_account_id",
        "external_account_id",
        5000,
        "idempotency_key",
    )
    assert response.status == PaymentStatus.PENDING