import datetime

from pydantic import Field
from schemas import BaseModelWithId
from schemas.string_eos import Operator


class RedirectCall(BaseModelWithId):
    eosTypeid: str = None
    dtRedirectTime_: datetime.datetime = datetime.datetime.now()
    dtRedirectConfirm_: datetime.datetime
    operator: Operator = None
    redirectCancel: bool
    newPhoneCallId: str
    conference: bool


class Phone(BaseModelWithId):
    phoneCallId: str = Field(default_factory=lambda: Phone._BaseModelWithId__get_next_id())
    dtSend_: datetime.datetime = datetime.datetime.now()
    operator: Operator = None
    OperatorIniciatied: bool
    dtCall_: datetime.datetime = datetime.datetime.now()
    dtConnect_: datetime.datetime | str = datetime.datetime.now()
    bCallEnded: bool = None
    aCallEnded: bool = None
    dtEndCall_: datetime.datetime = datetime.datetime.now()
    redirectCall: RedirectCall = None
