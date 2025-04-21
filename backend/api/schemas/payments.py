from pydantic import BaseModel
from enum import Enum
from uuid import UUID
from typing import Optional

# Enum for payment status
class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"

# PaymentResponse that represents the response from an external payment service
class PaymentResponse(BaseModel):
    payment_id: UUID
    status: PaymentStatus
    amount: int

# Request model to perform a payment (ACH Debit, ACH Credit, or Swipe)
class PaymentRequest(BaseModel):
    internal_account_id: str
    external_account_id: str
    amount: int  # Amount in cents (e.g., $50.00 = 5000)
    idempotency_key: str  # Used to prevent duplicate transactions
