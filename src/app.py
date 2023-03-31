import re
import aiocache
import os
import secrets

from datetime import datetime
from fastapi import FastAPI, Query, HTTPException
from dadata import Dadata
from dotenv import load_dotenv
from .connection import get_db_pool
from .models import User


app = FastAPI()
load_dotenv()
cache = aiocache.Cache(aiocache.Cache.MEMORY)


async def get_country_code(country: str):
    cached_code = await cache.get(country)
    if cached_code:
        return cached_code
    dadata = Dadata(os.getenv("TOKEN"))
    result = dadata.suggest("country", country)
    code = result[0]['data']['code']
    await cache.set(country, code)
    return code


@app.post("/save_user_data")
async def save_user_data(user: User):
    # проверяем данные на валидность
    if not all([
        re.match(r'^[а-яА-ЯёЁ\s-]+$', user.name),
        re.match(r'^[а-яА-ЯёЁ\s-]+$', user.surname),
        (user.patronymic is None or re.match(
            r'^[а-яА-ЯёЁ\s-]+$', user.patronymic)),
        user.phone_number.startswith("7"),
        (user.email is None or "@" in user.email),
        re.match(r'^[а-яА-ЯёЁ\s-]+$', user.country)
    ]):
        return {"error": "Invalid input data"}

    async with await get_db_pool() as conn:
        # проверяем, есть ли уже данные от этого пользователя
        existing_user = await conn.fetchrow(
            "SELECT * FROM users WHERE phone_number=$1", user.phone_number)
        if existing_user:
            # обновляем данные
            try:
                await conn.execute(
                    "UPDATE users SET name=$1, surname=$2, patronymic=$3, email=$4, country=$5, date_modified=$6 WHERE phone_number=$7",
                    user.name, user.surname, user.patronymic, user.email, user.country, datetime.now(), user.phone_number
                )
                user_id = existing_user["user_id"]
                date_created = existing_user["date_created"]
            except:
                return {"error": "U use same info"}
        else:
            # генерируем новый user_id
            user_id = str(secrets.token_hex(6))
            date_created = datetime.now()
            # сохраняем данные
            await conn.execute(
                "INSERT INTO users (user_id, name, surname, patronymic, phone_number, email, country, date_created) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)",
                user_id, user.name, user.surname, user.patronymic, user.phone_number, user.email, user.country, date_created
            )

    return {"user_id": user_id, "date_created": date_created, "date_modified": datetime.now()}


@app.get("/get_user_data")
async def get_user_data(phone_number: str = Query(...)):
    async with await get_db_pool() as conn:
        # проверяем, есть ли уже данные от этого пользователя
        existing_user = await conn.fetchrow(
            "SELECT * FROM users WHERE phone_number=$1", phone_number)
        if existing_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return {
            "name": existing_user['name'],
            "surname": existing_user['surname'],
            "patronymic": existing_user['patronymic'],
            "phone_number": existing_user['phone_number'],
            "email": existing_user['email'],
            "country": existing_user['country'],
            "country_code": await get_country_code(existing_user['country'])
        }


@app.delete("/delete_user_data")
async def delete_user_data(phone_number: str = Query(...)):
    async with await get_db_pool() as conn:
        existing_user = await conn.fetchrow(
            "SELECT * FROM users WHERE phone_number=$1", phone_number)
        if existing_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        else:
            await conn.execute(
                "DELETE FROM users Where phone_number=$1",
                phone_number
            )
        return{
            "succcess": "Success"
        }
