from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from backend.app.db import get_session
from backend.app.core.security import verify_password, get_password_hash, create_access_token
from backend.app.models.user import User, UserCreate, Token, UserRead

router = APIRouter()

@router.post("/register", response_model=UserRead)
def register(user_in: UserCreate, session: Session = Depends(get_session)):
    try:
        print(f"Registering user: {user_in.email}")
        statement = select(User).where(User.email == user_in.email)
        existing_user = session.exec(statement).first()
        if existing_user:
            print("User already exists")
            raise HTTPException(
                status_code=400,
                detail="The user with this email already exists in the system.",
            )
        
        print("Creating new user object")
        user = User(
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password),
            full_name=user_in.full_name,
            is_active=True
        )
        print("Adding to session")
        session.add(user)
        print("Committing")
        session.commit()
        print("Refreshing")
        session.refresh(user)
        print("User registered successfully")
        return user
    except Exception as e:
        print(f"ERROR in register: {e}")
        import traceback
        traceback.print_exc()
        raise e


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    statement = select(User).where(User.email == form_data.username)
    user = session.exec(statement).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(subject=user.email)
    return {"access_token": access_token, "token_type": "bearer"}
