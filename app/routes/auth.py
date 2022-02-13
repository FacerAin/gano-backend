from fastapi import APIRouter, Body, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import List
from app.db.staff import *
from app.models.staff import *
from app.models.auth import *
from app.util.auth import *
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


# 로그인
@router.post("/login", response_description="Login Staff")
async def login_staff(login_data: LoginScema = Body(...)):
    login_data = jsonable_encoder(login_data)
    account_id = login_data['account_id']
    account_password = login_data['account_password']
    staff = await get_staff_by_account_id(account_id)
    if not staff:
        raise HTTPException(
            status_code=401, detail=f"Staff {account_id} not found")
    is_verified = verify_password(account_password, staff['account_password'])
    if not is_verified:
        raise HTTPException(
            status_code=401, detail=f"Staff {account_id} Wrong Password")

    access_token = create_access_token(
        data={"sub": account_id}
    )

    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_staff(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        account_id: str = payload.get("sub")
        if account_id is None:
            raise credentials_exception
        token_data = TokenData(account_id=account_id)
    except JWTError:
        raise credentials_exception
    staff = get_staff_by_account_id(token_data.account_id)
    if staff is None:
        raise credentials_exception
    return staff
