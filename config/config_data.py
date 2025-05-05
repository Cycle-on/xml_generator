import os

from dotenv import load_dotenv

from constants import ALL_PROJ_CONSTANTS

load_dotenv()  # will be used with .env file
# if you want to take vars from global environment, start program in terminal
base_directory_name = "files"

output_directory_name: str = os.path.join(
    base_directory_name,
    ALL_PROJ_CONSTANTS["files_prefix"],
)
logs_directory_name = "errors"

SERVER_ADDRESS = os.getenv("SERVER_ADDRESS")
SERVER_PASSWORD = os.getenv("SERVER_PASSWORD")
SERVER_LOGIN = os.getenv("SERVER_LOGIN")

DATE_ZERO = None
