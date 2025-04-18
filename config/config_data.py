import os

from dotenv import load_dotenv

from constants import *

load_dotenv()  # will be used with .env file
# if you want to take vars from global environment, start program in terminal
base_directory_name = 'files'

output_directory_name: str = os.path.join(
    base_directory_name,
    files_prefix,
)
logs_directory_name = 'errors'

SERVER_ADDRESS = os.getenv('SERVER_ADDRESS')
SERVER_PASSWORD = os.getenv('SERVER_PASSWORD')
SERVER_LOGIN = os.getenv("SERVER_LOGIN")

DATE_ZERO = None