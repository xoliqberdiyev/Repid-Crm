import sys
import os

from database import models, session
from utils.hashing import Hasher
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

username = input('Username:')
password = input('Password:')
phone_number = input('Phone_number:')

async def create_super_user(username: str, password: str, phone_number: str):
    async with session.async_session() as db:  # Directly create an AsyncSession
        async with db.begin():  # Begin transaction
            new_user = models.Employees(
                username=username,
                password=Hasher.get_password_hash(password),
                phone_number=phone_number,
                position_id=1,
                user_type=models.UserType.admin
            )
            db.add(new_user)  # Add to session
        await db.commit()  # Commit transaction

    print("User created successfully")


async def main():
    await create_super_user(username=username,password=password,phone_number=phone_number)

asyncio.run(main()) 
print("User created successfully")

