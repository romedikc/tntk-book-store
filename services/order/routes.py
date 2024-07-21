from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from services.database import get_db
from services.order import crud
from services.order.schemas import Order, OrderCreate, OrderItemCreate, OrderItem, Payment, PaymentCreate
from services.rabbitmq_client import get_order_rabbitmq_client

# from services.rabbitmq_client import get_order_rabbitmq_client

db_dependency = Depends(get_db)
# rabbit_dependency = Depends(rabbitmq_client)

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/orders/", response_model=Order)
def create_order(order: OrderCreate,
                 db: Session = db_dependency,
                 rabbitmq_client: get_order_rabbitmq_client = Depends()):
    return crud.create_order(db=db, order=order, rabbitmq_client=rabbitmq_client)


@router.post("/orders/{order_id}/items/", response_model=OrderItem)
def add_order_item(order_id: int, item: OrderItemCreate, db: Session = db_dependency):
    return crud.add_order_item(db=db, order_id=order_id, item=item)


@router.post("/payments/", response_model=Payment)
def create_payment(payment: PaymentCreate, db: Session = db_dependency):
    return crud.create_payment(db=db, payment=payment)


@router.get("/orders/", response_model=List[Order])
def read_orders(db: Session = db_dependency):
    return crud.get_orders(db=db)


@router.get("/payments/", response_model=List[Payment])
def read_payments(db: Session = db_dependency):
    return crud.get_payments(db=db)
