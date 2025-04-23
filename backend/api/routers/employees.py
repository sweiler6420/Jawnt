from fastapi import APIRouter, HTTPException
from api.schemas.payments import PaymentRequest, PaymentResponse, PaymentStatus
from sqlalchemy.exc import SQLAlchemyError
from api.schemas.employees import *
from api.database import get_db
from api.queue.queue import queue
from typing import Tuple
from api.utils import *
import uuid
import time

# Router for employees
router = APIRouter()

# AUTHENTICATION INJECTION FOR ADMIN ENDPOINTS
def employee_required(x_organization_id: int = Header(...), x_employee_id: int = Header(...), db: Session = Depends(get_db)) -> OrganizationEmployee:
    try:
        employee = db.query(OrganizationEmployee).filter_by( organization_id=x_organization_id, id=x_employee_id).first()
        
        if not employee:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You must be an employee of this organization to access this resource.")
        
    except SQLAlchemyError as e:
        print(f"Database error occurred: {e}")
        raise HTTPException(status_code=500, detail="Database error while checking for existing employee.")
    
    # Return the header values as a tuple (or you could return an object)
    return employee


@router.post("/login", response_model=EmployeeLoginResponse)
def employee_login(payload: EmployeeLoginRequest, db: Session = Depends(get_db)):
    # 1. Lookup the organization by name
    try:
        org = db.query(Organization).filter(Organization.name == payload.organization_name).first()

        if not org:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
        
    except SQLAlchemyError as e:
        print(f"Database error occurred: {e}")
        raise HTTPException(status_code=500, detail="Database error while checking for existing organization.")

    # 2. Lookup the employee by email and org ID
    try:
        employee = db.query(OrganizationEmployee).filter(OrganizationEmployee.email == payload.email, OrganizationEmployee.organization_id == org.id).first()

        if not employee:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found in organization")
    
    except SQLAlchemyError as e:
        print(f"Database error occurred: {e}")
        raise HTTPException(status_code=500, detail="Database error while checking for existing employee.")
    
     # 3. Determine if the employee is an admin
    try:
        is_admin = db.query(OrganizationAdministrator).filter(OrganizationAdministrator.organization_id == org.id, OrganizationAdministrator.id == employee.id).first() is not None
    
    except SQLAlchemyError as e:
        print(f"Database error occurred: {e}")
        raise HTTPException(status_code=500, detail="Database error while checking for admin status.")

    return {
        "employee": {
            "id": employee.id,
            "first_name": employee.first_name,
            "last_name": employee.last_name,
            "email": employee.email,
            "is_admin": is_admin
        },
        "organization": org
    }


@router.get("/", response_model=OrganizationEmployeeResponse)
def get_employee(employee: OrganizationEmployee = Depends(employee_required), db: Session = Depends(get_db)):
    """Fetch an employee by ID along with their accounts and debit card information"""
      
    try:    
        # Query the internal and external accounts linked to the employee
        internal_account = db.query(OrganizationEmployeeAccount).filter(OrganizationEmployeeAccount.account_id == employee.id * 2).first()

        external_account = db.query(OrganizationEmployeeAccount).filter(OrganizationEmployeeAccount.account_id == employee.id * 2 + 1).first()

        if not internal_account or not external_account:
            raise HTTPException(status_code=404, detail="Employee accounts not found")
        
        # Query the debit card linked to the internal account
        debit_card = db.query(OrganizationEmployeeAccountDebitCard).filter(OrganizationEmployeeAccountDebitCard.debit_card_id == internal_account.account_id).first()

        if not debit_card:
            raise HTTPException(status_code=404, detail="Employee debit card not found")
        
        # Return the employee with account and debit card info
        return OrganizationEmployeeResponse(
            id=employee.id,
            first_name=employee.first_name,
            last_name=employee.last_name,
            email=employee.email,
            idempotency_key=str(randint(1, 10202)),
            internal_account=OrganizationEmployeeAccountResponse(
                account_id=internal_account.account_id,
                balance_cents=internal_account.balance_cents
            ),
            external_account=OrganizationEmployeeAccountResponse(
                account_id=external_account.account_id,
                balance_cents=external_account.balance_cents
            ),
            debit_card=OrganizationEmployeeAccountDebitCardResponse(
                debit_card_id=debit_card.debit_card_id
            )
        )
        
    except SQLAlchemyError as e:
        print(f"Database error occurred: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@router.get("/payments", response_model=List[OrganizationEmployeeAccountPaymentResponse])
def get_employee_payments(employee: OrganizationEmployee = Depends(employee_required), db: Session = Depends(get_db)):
    """Fetch an employee by ID along with their accounts and debit card information"""
    
    try:    
        payments = db.query(OrganizationEmployeeAccountPayment).filter_by(internal_account_id=int(employee.id*2)).all()

        if not payments:
            raise HTTPException(status_code=404, detail="No payments found for this employee")

        return payments
        
    except SQLAlchemyError as e:
        print(f"Database error occurred: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@router.get("/transactions", response_model=List[OrganizationEmployeeAccountDebitCardTransactionResponse])
def get_employee_payments(employee: OrganizationEmployee = Depends(employee_required), db: Session = Depends(get_db)):
    """Fetch an employee by ID along with their accounts and debit card information"""
    
    try:    
        transactions = db.query(OrganizationEmployeeAccountDebitCardTransaction).filter_by(debit_card_id=int(employee.id*2)).all()

        if not transactions:
            raise HTTPException(status_code=404, detail="No transactions found for this employee")

        return transactions
        
    except SQLAlchemyError as e:
        print(f"Database error occurred: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

# FastAPI endpoint to process ACH Debit payments
@router.post("/process-ach-debit", response_model=PaymentResponse)
async def process_ach_debit(payment: PaymentRequest, employee: OrganizationEmployee = Depends(employee_required)):
    """Endpoint to process an ACH Debit payment"""
    # First check the queue for a task with the same idempotency key
    if queue.has_task(payment.idempotency_key):
        raise HTTPException(status_code=409, detail="Payment with this idempotency key is already being processed.")
    
    try:
        result = perform_ach_debit(
            payment.internal_account_id,
            payment.external_account_id,
            payment.amount,
            payment.idempotency_key
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    payload = {
        "transaction_type": "payment",
        "type": "ACH_DEBIT",
        "status": result.status,
        "internal_account_id": payment.internal_account_id,
        "external_account_id": payment.external_account_id,
        "external_payment_id": result.payment_id,
        "amount_cents": result.amount
    }
    
    queue.publish(payment.idempotency_key, payload)
    
    return result


# FastAPI endpoint to process ACH Credit payments
@router.post("/process-ach-credit", response_model=PaymentResponse)
async def process_ach_credit(payment: PaymentRequest, employee: OrganizationEmployee = Depends(employee_required)):
    """Endpoint to process an ACH Credit payment"""
    if queue.has_task(payment.idempotency_key):
        raise HTTPException(status_code=409, detail="Payment with this idempotency key is already being processed.")
    
    try:
        result = perform_ach_credit(
            payment.internal_account_id,
            payment.external_account_id,
            payment.amount,
            payment.idempotency_key
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    payload = {
        "transaction_type": "payment",
        "type": "ACH_CREDIT",
        "status": result.status,
        "internal_account_id": payment.internal_account_id,
        "external_account_id": payment.external_account_id,
        "external_payment_id": result.payment_id,
        "amount_cents": result.amount
    }
    
    queue.publish(payment.idempotency_key, payload)

    return result

    

# FastAPI endpoint to process Debit Card Swipe payments
@router.post("/process-swipe", response_model=PaymentResponse)
async def process_swipe(payment: PaymentRequest, employee: OrganizationEmployee = Depends(employee_required)):
    """Endpoint to process a debit card swipe payment"""

    if queue.has_task(payment.idempotency_key):
        raise HTTPException(status_code=409, detail="Payment with this idempotency key is already being processed.")
    
    try:
        result = perform_swipe(
            payment.internal_account_id,  # Not used here, but included for consistency
            payment.amount,
            payment.idempotency_key
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    payload = {
        "transaction_type": "card",
        "status": result.status,
        "debit_card_id": payment.internal_account_id,
        "external_payment_id": result.payment_id,
        "amount_cents": result.amount
    }

    queue.publish(payment.idempotency_key, payload)
    
    return result
