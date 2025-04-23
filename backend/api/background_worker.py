# background_worker.py
import asyncio
from api.queue.queue import queue
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID
from api.database import SessionLocal
from api.schemas.payments import *
from api.utils import *

async def consume_queue_loop():
    while True:
        task = queue.consume()
        if task:
            task_id, payload = task
            print(f"Task with id: {task_id} now being processed")

            if payload["transaction_type"] == "card":
                await handle_card_task(task_id, payload)
            elif payload["transaction_type"] == "payment":
                await handle_payment_task(task_id, payload)
        await asyncio.sleep(15)


async def handle_payment_task(task_id: str, payload: dict):
    db = SessionLocal()

    payment_status = await get_payment_status(payload['external_payment_id'])

    if payment_status == PaymentStatus.FAILURE:
        print("Payment Failed")
        print("Adding Payment Back onto Queue")
        queue.publish(task_id, payload)
    elif payment_status == PaymentStatus.SUCCESS:
        print("Payment Succeeded")
        try:
            new_payment = OrganizationEmployeeAccountPayment(
                type=payload['type'],
                external_account_id=payload['external_account_id'],
                internal_account_id=payload['internal_account_id'],
                external_payment_id=payload['external_payment_id'],
                amount_cents=payload['amount_cents']
            )
            db.add(new_payment)
            db.commit()
            db.refresh(new_payment)
        except SQLAlchemyError as e:
            print(f"Database error occurred: {e}")
            db.rollback()


async def handle_card_task(task_id: str, payload: dict):
    db = SessionLocal()

    payment_status = await get_swipe_status(payload['external_payment_id'])

    if payment_status == PaymentStatus.FAILURE:
        print("Card Transaction Failed")
        print("Adding Transaction Back onto Queue")
        queue.publish(task_id, payload)
    elif payment_status == PaymentStatus.SUCCESS:
        print("Transaction Succeeded")
        try:
            new_payment = OrganizationEmployeeAccountDebitCardTransaction(
                debit_card_id=payload['debit_card_id'],
                external_payment_id=payload['external_payment_id'],
                merchant_name="Jawnt",
                amount_cents=payload['amount_cents']
            )
            db.add(new_payment)
            db.commit()
            db.refresh(new_payment)
        except SQLAlchemyError as e:
            print(f"Database error occurred: {e}")
            db.rollback()

