from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, aliased
from sqlalchemy import exists, select
import uuid
from api.utils import *
from api.schemas.organizations import *
from api.database import get_db  # You’ll need a `get_db` function to get the DB session
from api.models import *

router = APIRouter()


@router.post("/", response_model=CreateOrganizationResponse)
def create_organization(org: CreateOrganization, db: Session = Depends(get_db)):

    # Check for existing organization with the same name
    existing_org = db.query(Organization).filter(Organization.name == org.name).first()
    if existing_org:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"An organization with the name '{org.name}' already exists."
        )
    
    # Create our Org
    org_uid = str(uuid.uuid4())
    db_org = Organization(uid=org_uid, name=org.name)
    db.add(db_org)
    db.commit()
    db.refresh(db_org)

    # Create an Employee under that organization
    employee = OrganizationEmployee(
        organization_id=db_org.id,
        first_name=org.admin.first_name,
        last_name=org.admin.last_name,
        email=org.admin.email
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)

    # Create the admin using that employee 
    admin = OrganizationAdministrator(organization_id=db_org.id, employee_id=employee.id)
    db.add(admin)
    db.commit()

    # Return the organization with its admin
    return db_org


@router.get("/{organization_id}/employees", response_model=EmployeesListResponse)
def list_employees(organization_id: int, db: Session = Depends(get_db)):
    # Check if org exists
    org_exists = db.query(exists().where(Organization.id == organization_id)).scalar()
    if not org_exists:
        raise HTTPException(status_code=404, detail="Organization not found")

    # Get all employees for this organization
    employees = db.query(OrganizationEmployee).filter(OrganizationEmployee.organization_id == organization_id).all()

    # Get set of admin employee_ids for quick lookup
    admin_employee_ids = {
        admin.employee_id for admin in db.query(OrganizationAdministrator).filter(
            OrganizationAdministrator.organization_id == organization_id
        ).all()
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

    return {"employees": employee_list}