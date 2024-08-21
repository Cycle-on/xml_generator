import datetime

from pydantic import Field, BaseModel

from constants import files_prefix
from schemas import BaseModelWithId
from schemas.string_eos import Operator


class redirectCall(BaseModelWithId):
    eosClassTypeId: str = None
    dtRedirectTime: datetime.datetime = datetime.datetime.now()
    dtRedirectConfirm: datetime.datetime
    redirectCancel: bool
    bConference: bool
    Operator: Operator = None
    OperatorId: str = None
    PhoneCallId: str


class phoneCall(BaseModelWithId):
    phoneCallId: str = Field(default_factory=lambda: phoneCall._BaseModelWithId__get_next_id())
    dtSend: datetime.datetime = None
    bOperatorIniciatied: bool
    dtCall: datetime.datetime = datetime.datetime.now()
    dtConnect: datetime.datetime | str = None
    bCallEnded: bool = None
    aCallEnded: bool = None
    dtEndCall: datetime.datetime = datetime.datetime.now()
    OperatorId: str = None
    RedirectCall: redirectCall | None = None


class Call(BaseModelWithId):
    callId: str = Field(default_factory=lambda: f"{files_prefix}_{BaseModelWithId._BaseModelWithId__get_next_id()}")
    strCallStatus: str = None
    PhoneCall: phoneCall = None
    PhoneCallID: str | None = None
    dtCall: datetime.datetime
    dtSend: datetime.datetime = None


class Calls(BaseModel):
    Call: list[Call]
    dtSend: datetime.datetime = datetime.datetime.now()
