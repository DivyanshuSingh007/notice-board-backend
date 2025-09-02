from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
import logging
logging.basicConfig(level=logging.INFO)

from models import Users
from dependencies import get_db  
import os

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Security configs
# Read from environment for production; ensure to set SECRET_KEY on Render
SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-prod")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
ALLOW_MAKE_ADMIN = os.getenv("ALLOW_MAKE_ADMIN", "false").lower() in ("1", "true", "yes")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Custom form to use 'email' instead of 'username'
class OAuth2EmailRequestForm:
    def __init__(self, email: str = Form(...), password: str = Form(...)):
        self.email = email
        self.password = password

# JSON-based login request model
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

db_dependency = Annotated[Session, Depends(get_db)]

# ----------------------------------------
# Schemas
# ----------------------------------------

class CreateUserRequest(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=3)
    last_name: str = Field(..., min_length=3)
    mobile_no: str = Field(..., min_length=10)
    password: str = Field(..., min_length=8)
    admin: bool = False  # Allow admin flag in request, but restrict below

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    mobile_no: str
    admin: bool
    
    class Config:
        from_attributes = True

# ----------------------------------------
# Utilities
# ----------------------------------------

def authenticate_user(email: str, password: str, db: Session):
    user = db.query(Users).filter(Users.email == email).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(email: str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": email, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: db_dependency):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(Users).filter(Users.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# ----------------------------------------
# Routes
# ----------------------------------------

@router.post("/register")
def create_user(create_user_request: CreateUserRequest, db: db_dependency):
    logging.info(f"Registration attempt: {create_user_request.email}, mobile: {create_user_request.mobile_no}")
    existing_user = db.query(Users).filter(Users.email == create_user_request.email).first()
    if existing_user:
        logging.warning(f"Registration failed: Email already registered: {create_user_request.email}")
        raise HTTPException(status_code=400, detail="User already registered")
    existing_mobile = db.query(Users).filter(Users.mobile_no == create_user_request.mobile_no).first()
    if existing_mobile:
        logging.warning(f"Registration failed: Mobile number already registered: {create_user_request.mobile_no}")
        raise HTTPException(status_code=400, detail="Mobile number already registered")
    hashed_pw = bcrypt_context.hash(create_user_request.password)
    # Only allow admin if this is the first user
    is_first_user = db.query(Users).count() == 0
    is_admin = create_user_request.admin and is_first_user
    if create_user_request.admin and not is_first_user:
        logging.warning(f"Registration failed: Attempt to register admin after first user: {create_user_request.email}")
        raise HTTPException(status_code=403, detail="Admin can only be assigned to the first registered user.")
    new_user = Users(
        email=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        mobile_no=create_user_request.mobile_no,
        hashed_password=hashed_pw,
        admin=is_admin
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logging.info(f"User registered successfully: {new_user.email}, admin: {new_user.admin}")
    return {"message": "User registered successfully", "user_id": new_user.id}

@router.post("/login", response_model=TokenResponse)
def login(form_data: Annotated[OAuth2EmailRequestForm, Depends()], db: db_dependency):
    # Updated: Trigger Render redeployment for user deletion sync
    user = authenticate_user(form_data.email, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user.email)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/logout")
def logout(): 
    # For stateless JWT, logout is handled on the client by removing the token
    return {"message": "Logged out successfully. Please remove the token from your client."}

@router.get("/me")
def get_my_profile(current_user: Annotated[Users, Depends(get_current_user)]):
    return {
        "email": current_user.email,
        "name": f"{current_user.first_name} {current_user.last_name}",
        "mobile": current_user.mobile_no,
        "admin": current_user.admin
    }

@router.get("/admin-only")
def admin_only(current_user: Annotated[Users, Depends(get_current_user)]):
    if not current_user.admin:
        raise HTTPException(status_code=403, detail="Admins only")
    return {"message": f"Welcome Admin {current_user.first_name}!"}

@router.post("/make-admin")
def make_user_admin(email: str, db: db_dependency):
    """
    Elevate a user to admin by their email.
    Guarded by ALLOW_MAKE_ADMIN env flag. Keep disabled in production.
    """
    if not ALLOW_MAKE_ADMIN:
        raise HTTPException(status_code=403, detail="This endpoint is disabled in this environment")

    user = db.query(Users).filter(Users.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.admin = True
    db.commit()
    
    return {
        "message": f"User {email} is now an admin",
        "user_id": user.id,
        "admin": user.admin
    }

@router.get("/users", response_model=List[UserResponse])
def get_all_users(current_user: Annotated[Users, Depends(get_current_user)], db: db_dependency):
    """
    Get all users - Admin only endpoint
    """
    if not current_user.admin:
        raise HTTPException(status_code=403, detail="Only admins can view all users")
    
    users = db.query(Users).all()
    return users
