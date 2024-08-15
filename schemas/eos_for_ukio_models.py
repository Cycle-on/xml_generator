import datetime

from pydantic import Field
from schemas import BaseModelWithId


class card01(BaseModelWithId):
    card01Id: str = Field(default_factory=lambda: card01._BaseModelWithId__get_next_id())
    dtCreate: datetime.datetime
    # strIncidentType: IncidentType
    # strObject: str = None
    # bObjectGasified: bool = None


class card02(BaseModelWithId):
    card02Id: str = Field(default_factory=lambda: card02._BaseModelWithId__get_next_id())
    dtCreate: datetime.datetime


class card03(BaseModelWithId):
    card03Id: str = Field(default_factory=lambda: card03._BaseModelWithId__get_next_id())
    dtCreate: datetime.datetime


class card04(BaseModelWithId):
    card04Id: str = Field(default_factory=lambda: card04._BaseModelWithId__get_next_id())
    dtCreate: datetime.datetime
    dtConfirm: datetime.datetime


class cardCommServ(BaseModelWithId):
    cardCommServId: str = Field(default_factory=lambda: cardCommServ._BaseModelWithId__get_next_id())
    dtCreate: datetime.datetime


class cardAT(BaseModelWithId):
    cardATId: str = Field(default_factory=lambda: cardAT._BaseModelWithId__get_next_id())
    dtCreate: datetime.datetime
    # strInjurySuspect: str = None
