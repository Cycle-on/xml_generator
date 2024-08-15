import datetime

from pydantic import Field
from schemas import BaseModelWithId
from schemas.string_eos import Operator


class RedirectCall(BaseModelWithId):
    eosClassTypeId: str = None
    dtRedirectTime: datetime.datetime = datetime.datetime.now()
    dtRedirectConfirm: datetime.datetime
    redirectCancel: bool
    bConference: bool
    Operator: Operator = None
    OperatorId: str = None
    PhoneCallId: str


class PhoneCall(BaseModelWithId):
    phoneCallId: str = Field(default_factory=lambda: PhoneCall._BaseModelWithId__get_next_id())
    dtSend: datetime.datetime = datetime.datetime.now()
    bOperatorIniciatied: bool
    dtCall: datetime.datetime = datetime.datetime.now()
    dtConnect: datetime.datetime | str = datetime.datetime.now()
    bCallEnded: bool = None
    aCallEnded: bool = None
    dtEndCall: datetime.datetime = datetime.datetime.now()
    OperatorId: str = None
    RedirectCall: RedirectCall = None


class Call(BaseModelWithId):
    callId: str = Field(default_factory=lambda: BaseModelWithId._BaseModelWithId__get_next_id())
    strCallStatus: str = None
    PhoneCall: PhoneCall
    PhoneCallId: str
    dtCall: datetime.datetime
