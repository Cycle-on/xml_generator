import datetime
from typing import ClassVar

from pydantic import BaseModel, Field

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
    phoneCallId: str = Field(default_factory=lambda: Phone.__get_next_id())
    dtSend_: datetime.datetime = datetime.datetime.now()
    operator: Operator = None
    OperatorIniciatied: bool
    dtCall_: datetime.datetime = datetime.datetime.now()
    dtConnect_: datetime.datetime | str = datetime.datetime.now()
    bCallEnded: bool = None
    aCallEnded: bool = None
    dtEndCall_: datetime.datetime = datetime.datetime.now()
    redirectCall: RedirectCall = None

    __id_counter: ClassVar[int] = 0

    @classmethod
    def __get_next_id(cls):
        cls.__id_counter += 1
        return str(cls.__id_counter)
