from pydantic import BaseModel
from typing import List, Optional

# "/employees/login" POST
class EmployeeLoginRequest(BaseModel):
    organization_name: str
    email: str

class OrganizationResponse(BaseModel):
    id: int
    uid: str
    name: str

    class Config:
        from_attributes  = True

class EmployeeResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    is_admin: bool

class EmployeeLoginResponse(BaseModel):
    employee: EmployeeResponse
    organization: OrganizationResponse


# "/" GET
class OrganizationEmployeeAccountResponse(BaseModel):
    account_id: int
    balance_cents: int

class OrganizationEmployeeAccountDebitCardResponse(BaseModel):
    debit_card_id: int

class OrganizationEmployeeResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    idempotency_key: str
    internal_account: OrganizationEmployeeAccountResponse
    external_account: OrganizationEmployeeAccountResponse
    debit_card: OrganizationEmployeeAccountDebitCardResponse


# "/payments" GET
class OrganizationEmployeeAccountPaymentResponse(BaseModel):
    id: int
    type: str
    external_account_id: int
    internal_account_id: int
    external_payment_id: int
    amount_cents: int

    class Config:
        from_attributes  = True


# "/transactions" GET
class OrganizationEmployeeAccountDebitCardTransactionResponse(BaseModel):
    id: int
    debit_card_id: int
    external_payment_id: int
    merchant_name: str
    amount_cents: int

    class Config:
        from_attributes  = True