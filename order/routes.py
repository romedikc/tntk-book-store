import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from root.database import get_db
from order import crud
from order.schemas import Order, OrderCreate, OrderItemCreate, OrderItem, Payment, PaymentCreate
from order.utils import to_dict
from root.rabbitmq_client import get_order_rabbitmq_client
from root.redis import redis_client

db_dependency = Depends(get_db)

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/orders/", response_model=Order)
def create_order(order: OrderCreate,
                 db: Session = db_dependency,
                 rabbitmq_client: get_order_rabbitmq_client = Depends()):
    return crud.create_order(db=db, order=order, rabbitmq_client=rabbitmq_client)


@router.get("/user/{user_id}", response_model=List[Order])
def get_user_orders(user_id: int, db: Session = db_dependency):
    cache_key = f"user_orders_{user_id}"
    redis = redis_client.get_client()
    cached_orders = redis.get(cache_key)

    if cached_orders:
        return json.loads(cached_orders)

    orders = crud.get_user_orders(db=db, user_id=user_id)
    serialized_orders = [to_dict(order) for order in orders]
    # cache the orders
    redis.set(cache_key, json.dumps(serialized_orders), ex=3600)

    return orders


@router.delete("/user/{user_id}/cache")
def clear_user_orders_cache(user_id: int):
    return crud.clear_user_orders_cache(user_id)


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
