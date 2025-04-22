from pydantic import BaseModel, Field
from uuid import uuid4
from typing import Optional, List

# "/organizations" POST
class CreateAdminEmployee(BaseModel):
    first_name: str
    last_name: str
    email: str

class CreateOrganization(BaseModel):
    name: str
    admin: CreateAdminEmployee

class CreateOrganizationResponse(BaseModel):
    id: int
    uid: str
    name: str

    class Config:
        from_attributes  = True


# "/{organization_id}/employees" GET
class EmployeeResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    is_admin: bool

class EmployeesListResponse(BaseModel):
    employees: List[EmployeeResponse]