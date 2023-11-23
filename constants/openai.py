import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv('.env'))

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
