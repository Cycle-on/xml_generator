import datetime
import uuid
from decimal import Decimal

from pydantic import Field, BaseModel

from constants import files_prefix
from schemas import BaseModelWithId
from schemas.string_eos import Operator


class redirectCall(BaseModelWithId):
    redirectCallId: str = Field(default_factory=lambda: redirectCall._BaseModelWithId__get_next_id())
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
    phoneCall: PhoneCall = None
    PhoneCallID: str | None = None
    dtCall: datetime.datetime  #
    dtCallEnd: datetime.datetime = None  #
    aCallEnded: bool = None  #
    dtSend: datetime.datetime = None


class MissedCall(BaseModelWithId):
    missedCallId: str = Field(default_factory=lambda: BaseModelWithId._BaseModelWithId__get_next_id())
    dtCall: datetime.datetime
    dtSend: datetime.datetime
    dtCallEnd: datetime.datetime = None
    strCallEndReason: str = None
    strCgPN: str = None
    strAddressDevice: str = None
    appLatitude: Decimal = None
    appLongitude: Decimal = None
    appCoordAccuracy: int = None
    appLocAddress: str = None


class MissedCalls(BaseModel):
    missedCalls: list[MissedCall]
