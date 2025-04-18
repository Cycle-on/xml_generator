COEF_MIN = 50  # коэффициент на который будет умножаться кол во файлов для отправки
COEF_MAX = 150  # оба числа будут разделены на 100

SENDER_WORK_TYPE = 'by_delay'  # can be: 'by_delay' or 'by_date'
# print('sender')
SENDER_DELAY = 20  # seconds
# print(SENDER_DELAY, 'sender')
ALL_TIME = 2 * 60 * 60  # seconds

BASE_SOAP_PREFIX = """<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
<SOAP-ENV:Header/>
    <SOAP-ENV:Body>
"""
BASE_SOAP_POSTFIX = """    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>"""

UKIO_SOAP_PREFIX = ""
UKIO_SOAP_POSTFIX = ""

MISSED_SOAP_PREFIX = ""
MISSED_SOAP_POSTFIX = ""

ARMWORK_SOAP_PREFIX = ""
ARMWORK_SOAP_POSTFIX = ""

OPERATOR_WORK_SOAP_PREFIX = ""
OPERATOR_WORK_SOAP_POSTFIX = ""

INCIDENT_SOAP_PREFIX = ""
INCIDENT_SOAP_POSTFIX = ""
