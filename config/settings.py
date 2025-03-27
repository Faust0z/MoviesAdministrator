import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    raise FileNotFoundError(".env file not found. Please create one before running the app.")

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

required_vars = {"DB_USER", "DB_PASSWORD", "DB_HOST", "DB_NAME"}
missing_vars = [var for var in required_vars if not globals()[var]]

if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

DB_URI = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
