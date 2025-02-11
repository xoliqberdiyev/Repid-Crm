import asyncio
import logging
import sys
from os import getenv
import random

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as redis

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

from api.action import employee
from database import session as syc

TOKEN = "8180671290:AAEbM5zZp7W_tTZrllAaN0TW3YQI-gY9Tjw"

dp = Dispatcher()



class ForgotPasswordState(StatesGroup):
    waiting_for_phone = State()
    waiting_for_otp = State()

@dp.message(CommandStart())
async def start_command(message:Message):
    await message.answer("Welcome to changing password or say verify user",
    f"To get code type /forgot_password")

@dp.message(Command("forgot_password"))
async def start_forgot_password(message: Message, state: FSMContext):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Send Phone Number", request_contact=True)]], 
        resize_keyboard=True
    )
    await message.answer("Please share your phone number to reset your password.", reply_markup=keyboard)
    await state.set_state(ForgotPasswordState.waiting_for_phone)


@dp.message(ForgotPasswordState.waiting_for_phone)
async def process_phone_number(message: Message, state: FSMContext):
        phone_number = f'{message.contact.phone_number}'
        logging.info(phone_number)
        user_phone_number = await employee._get_phone_number(session=syc.async_session(), phone_number=phone_number)
    
        if user_phone_number != False:
             otp_code = str(random.randint(100000, 999999))
             await redis_client.set(f"user:{user_phone_number.phone_number}:phone", otp_code, ex=60)
             await message.answer(f"🔑 Your OTP code is: <b>{otp_code}</b>", reply_markup=ReplyKeyboardRemove())
        else:

            await message.answer('User not found with this phone number',reply_markup=ReplyKeyboardRemove())

        await state.update_data(phone=phone_number)
        
        await state.set_state(ForgotPasswordState.waiting_for_otp)

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())