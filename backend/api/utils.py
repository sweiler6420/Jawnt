from fastapi import Header, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.models import *
from api.schemas.payments import *
from random import randint
import uuid
import time 

# External call to simulate a payment service (mocked)
def external_call(amount: int) -> PaymentResponse:
    """Mock an external payment service call"""
    time.sleep(2)  # Simulating delay like a real external service call
    return PaymentResponse(
        payment_id=uuid.uuid4(),
        status=PaymentStatus.PENDING,
        amount=amount
    )


def long_external_call():
    time.sleep(30)


# Perform ACH Debit (mocked)
def perform_ach_debit(internal_account_id: str, external_account_id: str, amount: int, idempotency_key: str) -> PaymentResponse:
    """Process an ACH Debit"""
    return external_call(
        internal_account_id,
        external_account_id,
        idempotency_key,
        amount=amount,
        )



# Perform ACH Credit (mocked)
def perform_ach_credit(internal_account_id: str, external_account_id: str, amount: int, idempotency_key: str) -> PaymentResponse:
    """Process an ACH Credit"""
    return external_call(
        internal_account_id,
        external_account_id,
        idempotency_key,
        amount=amount,
        )



# Perform Swipe (mocked, assuming debit card swipe)
def perform_swipe(debit_card_id: str, amount: int, idempotency_key: str) -> PaymentResponse:
    """Process a debit card swipe"""
    #TODO: This was given directly in the example but perhaps i need to get the internal/external ids from the debit card id. 
    return external_call(
        internal_account_id,
        external_account_id,
        idempotency_key,
        amount=amount,
        )


def get_swipe_status(payment_id: str) -> PaymentStatus:
    long_external_call()
    return(
        PaymentStatus.SUCCESS if randint(1,2) == 1 else PaymentStatus.FAILURE
    )
    

def get_next_id(model, column, db):
    max_id = db.query(sa.func.max(getattr(model, column))).scalar()
    return (max_id or 100000) + 1
