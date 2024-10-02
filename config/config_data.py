import datetime
import os
from constants import *
from dotenv import load_dotenv

load_dotenv()  # will be used with .env file
# if you want to take vars from global environment, start program in terminal
base_directory_name = 'files'

output_directory_name: str = os.path.join(
    base_directory_name,
    f'file_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}'
)
logs_directory_name = 'errors'

SERVER_ADDRESS = os.getenv('SERVER_ADDRESS')
SERVER_PASSWORD = os.getenv('SERVER_PASSWORD')
SERVER_LOGIN = os.getenv("SERVER_LOGIN")

# print(SERVER_ADDRESS, SERVER_PASSWORD, SERVER_LOGIN)
try:
    DATE_ZERO = datetime.datetime.strptime(DATE_ZERO_FORMAT, "%Y-%m-%d_%H-%M-%S")
except ValueError:
    print("Дата не соответствует формату YYYY-MM-DD_HH-MM-SS\nРабота прервана")
    quit()
