from dotenv import load_dotenv
from os import getenv

load_dotenv(dotenv_path='dataSensible.env')


BASE_URL = getenv('BASE_URL')