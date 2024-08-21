import datetime
import os
from constants import *

base_directory_name = 'files'

output_directory_name: str = os.path.join(
    base_directory_name,
    f'file_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}'
)
logs_directory_name = 'errors'
try:
    DATE_ZERO = datetime.datetime.strptime(DATE_ZERO_FORMAT, "%Y-%m-%d_%H-%M-%S")
except ValueError:
    print("Дата не соответствует формату YYYY-MM-DD_HH-MM-SS\nРабота прервана")
    quit()
