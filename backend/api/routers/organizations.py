from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, aliased
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import exists, select
import uuid
from api.utils import *
from api.schemas.organizations import *
from api.database import get_db
from api.models import *

router = APIRouter()

@router.post("/", response_model=CreateOrganizationResponse)
def create_organization(org: CreateOrganization, db: Session = Depends(get_db)):

    try:
        # Check for existing organization with the same name
        existing_org = db.query(Organization).filter(Organization.name == org.name).first()

        if existing_org:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"An organization with the name '{org.name}' already exists.")
        
    except SQLAlchemyError as e:
        print(f"Database error occurred: {e}")
        raise HTTPException(status_code=500, detail="Database error while checking for existing organization.")
    
    try:
        # Create our Org
        org_uid = str(uuid.uuid4())
        db_org = Organization(uid=org_uid, name=org.name)
        db.add(db_org)
        db.flush()
        
        # Create an Employee under that organization
        employee = OrganizationEmployee(
            organization_id=db_org.id,
            first_name=org.admin.first_name,
            last_name=org.admin.last_name,
            email=org.admin.email
        )
        db.add(employee)
        db.flush()

        # Create the admin using that employee 
        admin = OrganizationAdministrator(id=employee.id, organization_id=db_org.id)
        db.add(admin)

        # 2. Create internal employee bank account
        # Caveat stated in create_employee endpoint in administrators.py
        internal_account = OrganizationEmployeeAccount(
            organization_id=db_org.id,
            account_id=employee.id * 2,
            balance_cents=0
        )
        db.add(internal_account)

        external_account = OrganizationEmployeeAccount(
            organization_id=db_org.id,
            account_id=employee.id * 2 + 1,
            balance_cents=0
        )
        db.add(external_account)

        # 3. Create debit card linked to the internal account
        debit_card = OrganizationEmployeeAccountDebitCard(
            organization_id=db_org.id,
            debit_card_id=internal_account.account_id
        )
        db.add(debit_card)

        db.commit()

        db.refresh(db_org)
        db.refresh(employee)
        db.refresh(admin)

    except SQLAlchemyError as e:
        print(f"Database error occurred: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")

    # Return the organization with its admin
    return db_org


@router.get("/{organization_id}/employees", response_model=EmployeesListResponse)
def list_employees(organization_id: int, db: Session = Depends(get_db)):
    # Check if org exists
    try:
        org_exists = db.query(exists().where(Organization.id == organization_id)).scalar()

        if not org_exists:
            raise HTTPException(status_code=404, detail="Organization not found")
    
    except SQLAlchemyError as e:
        print(f"Database error occurred: {e}")
        raise HTTPException(status_code=500, detail="Database error while checking for existing employee.")
    
    try:
        # Get all employees for this organization
        employees = db.query(OrganizationEmployee).filter(OrganizationEmployee.organization_id == organization_id).all()

        # Get set of admin employee_ids for quick lookup
        admin_employee_ids = {
            admin.id for admin in db.query(OrganizationAdministrator).filter(OrganizationAdministrator.organization_id == organization_id).all()
        }

        # Build response
        employee_list = [
            EmployeeResponse(
                id=e.id,
                first_name=e.first_name,
                last_name=e.last_name,
                email=e.email,
                is_admin=e.id in admin_employee_ids
            ) for e in employees
        ]
    
    except SQLAlchemyError as e:
        print(f"Database error occurred: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return {"employees": employee_list}