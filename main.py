import uvicorn
import os
from dotenv import load_dotenv
from src.app import app

if __name__ == "__main__":
    load_dotenv() # загружаем переменные окружения из .env файла
    uvicorn.run(app, host="0.0.0.0", port=8000)
