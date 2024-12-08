import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
POSTGRES_HOST = os.getenv("PGHOST")
POSTGRES_PORT = os.getenv("PGPORT")
POSTGRES_USER = os.getenv("PGUSER")
POSTGRES_PASSWORD = os.getenv("PGPASSWORD")
POSTGRES_DB = os.getenv("PGDATABASE")

# Construct database URL
DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Bot and API configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI configuration
GPT_MODEL = "gpt-4"  # Using GPT-4 for better response quality
