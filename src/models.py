from pydantic import BaseModel

class User(BaseModel):
    name: str
    surname: str
    patronymic: str = None
    phone_number: str
    email: str = None
    country: str
