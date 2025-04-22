from fastapi import APIRouter, HTTPException
from api.schemas.adminstrators import *
from api.utils import *
from api.models import *
from typing import Tuple
from api.database import get_db
import uuid
import time

# Router for administrators
router = APIRouter()

# AUTHENTICATION INJECTION FOR ADMIN ENDPOINTS
def admin_required(x_organization_id: int = Header(...), x_employee_id: int = Header(...), db: Session = Depends(get_db)) -> Tuple[int, int]:
    admin = db.query(OrganizationAdministrator).filter_by(
        organization_id=x_organization_id,
        employee_id=x_employee_id
    ).first()
    
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must be an admin to access this resource."
        )
    
    # Return the header values as a tuple (or you could return an object)
    return x_organization_id, x_employee_id


@router.post("/organizations/employees", response_model=EmployeeResponse)
def create_employee(employee_data: NewEmployeeRequest, headers: Tuple[int, int] = Depends(admin_required), db: Session = Depends(get_db)):
    org_id, user_id = headers

    employee_exists = db.query(OrganizationEmployee).filter(OrganizationEmployee.email == employee_data.email).first()

    if employee_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"An employee with the email '{employee_data.email}' already exists.")

    # 1. Create the employee
    new_employee = OrganizationEmployee(
        organization_id=org_id,
        first_name=employee_data.first_name,
        last_name=employee_data.last_name,
        email=employee_data.email
    )
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    # 2. Create internal employee bank account
    internal_account = OrganizationEmployeeAccount(
        organization_id=org_id,
        account_id=get_next_id(OrganizationEmployeeAccount, 'account_id', db),
        balance_cents=0
    )
    db.add(internal_account)
    db.commit()
    db.refresh(internal_account)

    # 3. Create debit card linked to that internal account
    debit_card = OrganizationEmployeeAccountDebitCard(
        organization_id=org_id,
        debit_card_id=get_next_id(OrganizationEmployeeAccountDebitCard, 'debit_card_id', db)
    )
    db.add(debit_card)
    db.commit()

    return new_employee


@router.put("/organizations/employees/{employee_id}", response_model=EmployeeResponse)
def create_employee(employee_id: int, update_data: EmployeeUpdateRequest, headers: Tuple[int, int] = Depends(admin_required), db: Session = Depends(get_db)):
    employee = db.query(OrganizationEmployee).filter(OrganizationEmployee.id == employee_id).first()

    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    
    # Update the employee's first and last name
    employee.first_name = update_data.first_name
    employee.last_name = update_data.last_name
    
    # Commit the changes to the database
    db.commit()
    db.refresh(employee)  # Refresh the employee instance with updated data
    
    # Return the updated employee
    return employee  # Return the updated employee to the client


@router.delete("/organizations/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int, headers: Tuple[int, int] = Depends(admin_required), db: Session = Depends(get_db)):
    org_id, user_id = headers

    # Check if the employee exists within the organization
    employee = db.query(OrganizationEmployee).filter(
        OrganizationEmployee.id == employee_id,
        OrganizationEmployee.organization_id == org_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found in the specified organization."
        )

    # Delete the associated accounts of the employee
    # First, delete the debit cards linked to the employee's accounts
    #TODO: This is where some more data model changes are required. Theres not really any linking keys between accounts and employees
    debit_cards = db.query(OrganizationEmployeeAccountDebitCard).filter(
        OrganizationEmployeeAccountDebitCard.organization_id == org_id,
        OrganizationEmployeeAccountDebitCard.account_id == employee.id
    ).all()

    for debit_card in debit_cards:
        db.delete(debit_card)

    # Then, delete the employee's internal account
    accounts = db.query(OrganizationEmployeeAccount).filter(
        OrganizationEmployeeAccount.organization_id == org_id,
        OrganizationEmployeeAccount.account_id == employee.id
    ).all()

    for account in accounts:
        db.delete(account)

    # Finally, delete the employee from the OrganizationEmployee table
    db.delete(employee)

    # Commit all deletions to the database
    db.commit()

    return {"detail": "Employee and their accounts have been successfully deleted."}