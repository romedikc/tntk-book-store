from typing import Annotated, List

from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from auth import schemas, crud
from auth.utils import verify_password, create_access_token
from root.database import get_db
from root.models import User

db_dependency = Annotated[Session, Depends(get_db)]
router = APIRouter(
    prefix="/auth",
    tags=["users"]
)


@router.post("/login", response_model=schemas.Token)
def login(db: db_dependency, userdetails: OAuth2PasswordRequestForm = Depends()):
    user = db.query(User).filter(User.email == userdetails.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"The User Does not exist")
    if not verify_password(userdetails.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="The Passwords do not match")
    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: db_dependency):
    db_user = crud.create_user(db=db,
                               name=user.name,
                               email=user.email,
                               password=user.password,
                               )
    return db_user


@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: db_dependency):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user


@router.patch("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: db_dependency):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return crud.update_user(db, db_user=db_user, user_update=user_update)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: db_dependency):
    if not crud.delete_user(db, user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.get("/users/", response_model=List[schemas.User])
def read_users(db: db_dependency):
    return crud.get_users(db)
