from sqlalchemy.orm import Session

from services.books.schemas import ProductUpdate
from services.models import Product


def create_product(db: Session,
                   name: str,
                   description: str,
                   price: float,
                   picture: str,
                   ):
    db_product = Product(name=name,
                         description=description,
                         price=price,
                         picture=picture,
                         )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def read_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def update_product(db: Session, product_id: int, product: ProductUpdate):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        for key, value in product.dict(exclude_unset=True).items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
        return db_product
    return None


def delete_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
        return True
    return False


def read_products(db: Session):
    return db.query(Product).all()
