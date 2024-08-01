import datetime

from pydantic import BaseModel

from schemas import Operator


class RedirectCall(BaseModel):
    eosTypeid: str = None
    dtRedirectTime_: datetime.datetime = datetime.datetime.now()
    dtRedirectConfirm_: datetime.datetime
    operator: Operator = None
    redirectCancel: bool
    newPhoneCallId: str
    conference: bool


class Phone(BaseModel):
    phoneCallId: str
    dtSend_: datetime.datetime = datetime.datetime.now()
    operator: Operator = None
    OperatorIniciatied: bool
    dtCall_: datetime.datetime = datetime.datetime.now()
    dtConnect_: datetime.datetime | str = datetime.datetime.now()
    bCallEnded: bool = None
    aCallEnded: bool = None
    dtEndCall_: datetime.datetime = datetime.datetime.now()
    redirectCall: RedirectCall = None
