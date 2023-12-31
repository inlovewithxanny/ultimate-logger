from dotenv import load_dotenv
from os import getenv

load_dotenv("./venv/.env")

TOKEN = getenv("TOKEN")

DEV_GUILDS = (1171526838795898920,)

MYSQL_USER = getenv("MYSQL_USER")
MYSQL_PASSWORD = getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = getenv("MYSQL_DATABASE")
MYSQL_HOST = getenv("MYSQL_HOST")
MYSQL_PORT = getenv("MYSQL_PORT")
