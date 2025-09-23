# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "clave_segura")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "registrodeudores")
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = os.getenv("CSRF_SECRET", "otra_clave_segura")