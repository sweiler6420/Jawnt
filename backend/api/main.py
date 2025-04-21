from fastapi import FastAPI
import time
from random import randint
from uuid import UUID
from api.routers import administrators, employees, payments

app = FastAPI()

# Include the administrators and employees routers
app.include_router(administrators.router, prefix="/admin", tags=["administrators"])
app.include_router(employees.router, prefix="/employee", tags=["employees"])
app.include_router(payments.router, prefix="/payment", tags=["payment"])

