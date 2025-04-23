from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import SQLAlchemyError
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
    try:
        admin = db.query(OrganizationAdministrator).filter_by( organization_id=x_organization_id, id=x_employee_id).first()
        
        if not admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You must be an admin to access this resource.")
        
    except SQLAlchemyError as e:
        print(f"Database error occurred: {e}")
        raise HTTPException(status_code=500, detail="Database error while checking for existing admin.")
    
    # Return the header values as a tuple (or you could return an object)
    return x_organization_id, x_employee_id


@router.post("/organizations/employees", response_model=EmployeeResponse)
def create_employee(employee_data: NewEmployeeRequest, headers: Tuple[int, int] = Depends(admin_required), db: Session = Depends(get_db)):
    org_id, user_id = headers

    try:
        employee_exists = db.query(OrganizationEmployee).filter(OrganizationEmployee.email == employee_data.email).first()

        if employee_exists:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"An employee with the email '{employee_data.email}' already exists.")
    
    except SQLAlchemyError as e:
        print(f"Database error occurred: {e}")
        raise HTTPException(status_code=500, detail="Database error while checking for existing employee.")


    try:
        # 1. Create the employee
        new_employee = OrganizationEmployee(
            organization_id=org_id,
            first_name=employee_data.first_name,
            last_name=employee_data.last_name,
            email=employee_data.email
        )
        db.add(new_employee)
        db.flush()

        # 2. Create internal employee bank account
        # Since there is no soft or hard relationship allowed in the data model i will create a decipherable int that uniquely identifies
        # Employees internal and external accounts. 
        # Internal accounts will be Even
        # External accounts will be Odd
        # employee_id * 2 as the base. 
        internal_account = OrganizationEmployeeAccount(
            organization_id=org_id,
            account_id=new_employee.id * 2,
            balance_cents=0
        )
        db.add(internal_account)

        external_account = OrganizationEmployeeAccount(
            organization_id=org_id,
            account_id=new_employee.id * 2 + 1,
            balance_cents=0
        )
        db.add(external_account)

        # 3. Create debit card linked to the internal account
        # Again, in order to link this with the employee, i will use the internal account's id as the debit card id
        # I know this is not realistic but it does fit in the parameters of the proposed features
        debit_card = OrganizationEmployeeAccountDebitCard(
            organization_id=org_id,
            debit_card_id=internal_account.account_id
        )
        db.add(debit_card)

        # Commit the changes
        db.commit()

        # Refresh the objs, technically should only need to refresh new_employee obj here
        db.refresh(new_employee)
        db.refresh(internal_account)
        db.refresh(external_account)
        db.refresh(debit_card)

    except SQLAlchemyError as e:
        print(f"Database error occurred: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return new_employee


@router.put("/organizations/employees/{employee_id}", response_model=EmployeeResponse)
def update_employee(employee_id: int, update_data: EmployeeUpdateRequest, headers: Tuple[int, int] = Depends(admin_required), db: Session = Depends(get_db)):
    try:
        employee = db.query(OrganizationEmployee).filter(OrganizationEmployee.id == employee_id).first()

        if not employee:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    
    except SQLAlchemyError as e:
        print(f"Database error occurred: {e}")
        raise HTTPException(status_code=500, detail="Database error while checking for existing employee.")
    
    try:
        # Update the employee's first and last name
        employee.first_name = update_data.first_name
        employee.last_name = update_data.last_name
        
        # Commit the changes to the database
        db.commit()
        db.refresh(employee)  # Refresh the employee instance with updated data

    except SQLAlchemyError as e:
        print(f"Database error occurred: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    # Return the updated employee
    return employee  # Return the updated employee to the client


@router.delete("/organizations/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int, headers: Tuple[int, int] = Depends(admin_required), db: Session = Depends(get_db)):
    org_id, user_id = headers

    try:
        # 1. Get the employee and validate they exist in this org
        employee = db.query(OrganizationEmployee).filter(OrganizationEmployee.id == employee_id, OrganizationEmployee.organization_id == org_id).first()

        if not employee:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found in the specified organization.")
        
    except SQLAlchemyError as e:
        print(f"Database error occurred: {e}")
        raise HTTPException(status_code=500, detail="Database error while checking for existing employee.")
    
    try:
        # 2. Calculate account IDs using your convention
        internal_account_id = employee.id * 2
        external_account_id = employee.id * 2 + 1

        # 3. Delete debit card (uses internal_account_id as debit_card_id)
        debit_card = db.query(OrganizationEmployeeAccountDebitCard).filter_by(
            organization_id=org_id,
            debit_card_id=internal_account_id
        ).first()
        if debit_card:
            db.delete(debit_card)

        # 4. Delete internal and external accounts
        accounts = db.query(OrganizationEmployeeAccount).filter(OrganizationEmployeeAccount.organization_id == org_id, OrganizationEmployeeAccount.account_id.in_([internal_account_id, external_account_id])).all()
        
        for account in accounts:
            db.delete(account)

        # 5. Delete the employee
        db.delete(employee)

        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        print(f"Database error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    return {"detail": "Employee and their accounts have been successfully deleted."}