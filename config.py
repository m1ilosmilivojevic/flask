# config.py
import os
from dotenv import load_dotenv, find_dotenv

# Load .env for local dev (ignored in prod)
load_dotenv(find_dotenv())

class Config:
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    SECRET_KEY = os.getenv("SECRET_KEY", "insecure-temp-key")
