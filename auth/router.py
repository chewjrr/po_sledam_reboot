from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth.schemas import UserCreate, UserLogin, Token
from auth.crud import create_user, get_user_by_email
from auth.utils import verify_password
from core.security import create_access_token
from db.session import SessionLocal
from auth.deps import get_db


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Проверка email
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Создание пользователя
    try:
        new_user = create_user(db, user)
    except Exception as e:
        # Логирование ошибки (в продакшене — через logging)
        print(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )

    # Выдача токена сразу после регистрации
    access_token = create_access_token(data={"sub": str(new_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token(data={"sub": str(db_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}