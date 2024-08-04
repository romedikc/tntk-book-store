from sqlalchemy.orm import Session

from auth import schemas
from auth.utils import hash_pass
from root.models import User


def create_user(db: Session, name: str, email: str, password: str):
    db_user = User(name=name,
                   email=email,
                   password=hash_pass(password),

                   )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def update_user(db: Session, db_user: User, user_update: schemas.UserUpdate):
    for field, value in user_update.dict().items():
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False


def get_users(db: Session):
    return db.query(User).all()
