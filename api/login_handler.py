# login with username and password.
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import get_db
from dals import user_dal

from utils.hashing import Hasher
from utils.security import create_access_token
from database.schemas import Token, ShowCurrentUser
from database import models
from utils import settings
from tg_main import redis_client
from api.action import employee

from jose import jwt, JWTError

oauth_token = OAuth2PasswordBearer('/login/access_token')

login_user = APIRouter()

async def get_redis():
    return redis_client

async def _get_user_username_auth(username: str, session: AsyncSession):
    async with session.begin():
        dal_of_user = user_dal.EmployeeDal(session)
        return await dal_of_user.get_username(
            username=username
        )

async def authenticate_user(email: str, password: str, db: AsyncSession):
    user = await _get_user_username_auth(username=email, session=db)

    if user is None:
        return
    if not Hasher.verify_password(password, user.password):
        return
    return user

async def get_current_user_from_token(token: str = Depends(oauth_token), db: AsyncSession = Depends(get_db)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='something woorgn fucking'
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get('sub')

        if username is None:
            raise credential_exception
    except JWTError:
        raise credential_exception

    user = await _get_user_username_auth(username=username, session=db)
    if user is None:
        raise credential_exception
    return user

@login_user.post('/access_token', response_model=Token)
async def get_user_token(user_form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(user_form.username, user_form.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    try:
        acces_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username, "type": user.user_type},
            expires_delta=acces_token_expires,
        )
    except ValueError as e:
        return f'Error on: {e}'
    return {"access_token": access_token, "type": "bearer"}

@login_user.get('/get-current-user', response_model=ShowCurrentUser)
async def get_current_user(
    current_user: models.Employees = Depends(get_current_user_from_token)
):
    """
    Endpoint to get the currently authenticated user.
    Requires a valid access token in the `Authorization` header.
    """
    return ShowCurrentUser(
        id=current_user.id,
        last_name=current_user.last_name,
        first_name=current_user.first_name,
        image=f'uploads/{current_user.image}',
        user_type=current_user.user_type
    )

@login_user.post('/change-password')
async def change_password(otp_code:str, your_new_password:str,redis=Depends(get_redis),
                          current_user: models.Employees = Depends(get_current_user_from_token),
                          db: AsyncSession = Depends(get_db)):
    valid_phone_number = await redis.get(f"user:{current_user.phone_number}:phone")
    print(valid_phone_number)

    if valid_phone_number == otp_code:
        return await employee._change_user_password(sesion=db,new_password=your_new_password,user_id=current_user.id)

    return {'message':'Something is wrong'}
