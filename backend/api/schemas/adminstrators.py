from pydantic import BaseModel

# "/organizations/{organization_id}/employees" POST
class NewEmployeeRequest(BaseModel):
    first_name: str
    last_name: str
    email: str # typically would like to use EmailStr from pydantic

class EmployeeResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    organization_id: int


# "/organizations/{organization_id}/employees" PUT
class EmployeeUpdateRequest(BaseModel):
    first_name: str
    last_name: str