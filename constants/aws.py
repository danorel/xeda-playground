import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv('.env'))

AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")
AWS_REGION = os.environ.get("AWS_REGION")
AWS_BUCKET = os.environ.get("AWS_BUCKET")
