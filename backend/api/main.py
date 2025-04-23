from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time
from random import randint
from uuid import UUID
from api.routers import administrators, employees, payments, organizations
from api import models
from api.database import engine
from api.queue.queue import queue
from api.background_worker import consume_queue_loop
import asyncio

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for your use case (e.g., React URL)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the administrators and employees routers
app.include_router(organizations.router, prefix="/organization", tags=["organization"])
app.include_router(administrators.router, prefix="/admin", tags=["administrators"])
app.include_router(employees.router, prefix="/employee", tags=["employees"])
app.include_router(payments.router, prefix="/payment", tags=["payment"])

@app.on_event("startup")
async def startup_event():
    # Start the consumer task in the background
    asyncio.create_task(consume_queue_loop())


@app.get("/")
def root():
    return {"message": "Hello, world!"}