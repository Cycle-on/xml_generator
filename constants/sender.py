SENDER_WORK_TYPE = 'by_delay'  # can be: 'by_delay' or 'by_date'
SENDER_DELAY = 3  # seconds

BASE_SOAP_PREFIX = """<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="s112">
    <SOAP-ENV:Body>
"""
BASE_SOAP_POSTFIX = """    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>"""

UKIO_SOAP_PREFIX = """<?сбитый префикс для ukio version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="s112">
    <SOAP-ENV:Body>"""
UKIO_SOAP_POSTFIX = ""

MISSED_SOAP_PREFIX = ""
MISSED_SOAP_POSTFIX = ""

ARMWORK_SOAP_PREFIX = ""
ARMWORK_SOAP_POSTFIX = ""

OPERATOR_WORK_SOAP_PREFIX = ""
OPERATOR_WORK_SOAP_POSTFIX = ""

INCIDENT_SOAP_PREFIX = ""
INCIDENT_SOAP_POSTFIX = ""
