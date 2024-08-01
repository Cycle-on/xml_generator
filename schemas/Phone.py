import datetime

from pydantic import BaseModel

from schemas import Operator


class RedirectCall(BaseModel):
    eosTypeid: str = ''
    dtRedirectTime_: datetime.datetime = datetime.datetime.now()
    dtRedirectConfirm_: datetime.datetime
    operator: Operator = ''
    redirectCancel: bool
    newPhoneCallId: str
    conference: bool


class Phone(BaseModel):
    phoneCallId: str
    dtSend_: datetime.datetime = datetime.datetime.now()
    operator: Operator = ''
    OperatorIniciatied: bool
    dtCall_: datetime.datetime = datetime.datetime.now()
    dtConnect_: datetime.datetime | str
    bCallEnded: bool
    aCallEnded: bool
    dtEndCall_: datetime.datetime = datetime.datetime.now()
    redirectCall: RedirectCall
