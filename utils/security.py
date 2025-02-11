from datetime import datetime
from datetime import timedelta
from typing import Optional

from jose import jwt
import re

from utils import settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def is_valid_phone_number(phone_number):
    # Regex to check valid phone number.
    pattern = r"^[+]{1}(?:[0-9\\-\\(\\)\\/" \
              "\\.]\\s?){6,15}[0-9]{1}$"
 
    # If the phone number is empty return false
    if not phone_number:
        return False
 
    # Return true if the phone number
    # matched the Regex
    if re.match(pattern, phone_number):
        return True
    else:
        return False