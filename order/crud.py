from fastapi import HTTPException
from sqlalchemy.orm import Session

from root.models import User, Order, Product, OrderItem, Payment
from order.schemas import OrderCreate, OrderItemCreate, PaymentCreate
from root.redis import redis_client


def create_order(db: Session, order: OrderCreate, rabbitmq_client):
    db_user = db.query(User).filter(User.id == order.user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_order = Order(user_id=order.user_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    for item in order.items:
        db_product = db.query(Product).filter(Product.id == item.product_id).first()
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")

        db_item = OrderItem(order_id=db_order.id, product_id=item.product_id, quantity=item.quantity)
        db.add(db_item)
        rabbitmq_client.publish({
            "order_id": db_order.id,
            "product_id": item.product_id,
            "quantity": item.quantity,
        })
    db.commit()

    db.refresh(db_order)
    return db_order


def add_order_item(db: Session, order_id: int, item: OrderItemCreate):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    db_product = db.query(Product).filter(Product.id == item.product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    db_item = OrderItem(order_id=order_id, product_id=item.product_id, quantity=item.quantity)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_payment(db: Session, payment: PaymentCreate):
    db_order = db.query(Order).filter(Order.id == payment.order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    db_payment = Payment(order_id=payment.order_id, amount=payment.amount, payment_method=payment.payment_method)
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)

    return db_payment


def get_orders(db: Session):
    return db.query(Order).all()


def get_payments(db: Session):
    return db.query(Payment).all()


def get_user_orders(db: Session, user_id: int):
    return db.query(Order).filter(Order.user_id == user_id).all()


def clear_user_orders_cache(user_id: int):
    cache_key = f"user_orders_{user_id}"
    redis = redis_client.get_client()
    redis.delete(cache_key)
    return {"message": "Cache cleared"}
