import datetime

from pydantic import Field
from schemas import BaseModelWithId

class Card01(BaseModelWithId):
    card01Id: str = Field(default_factory=lambda: Card01._BaseModelWithId__get_next_id())
    dtCreate: datetime.datetime
    # strIncidentType: IncidentType
    # strObject: str = None
    # bObjectGasified: bool = None


class Card02(BaseModelWithId):
    card02Id: str = Field(default_factory=lambda: Card02._BaseModelWithId__get_next_id())
    dtCreate: datetime.datetime


class Card03(BaseModelWithId):
    card03Id: str = Field(default_factory=lambda: Card03._BaseModelWithId__get_next_id())
    dtCreate: datetime.datetime


class Card04(BaseModelWithId):
    card04Id: str = Field(default_factory=lambda: Card04._BaseModelWithId__get_next_id())
    dtCreate: datetime.datetime
    dtConfirm: datetime.datetime


class CardCommServ(BaseModelWithId):
    cardCommServId: str = Field(default_factory=lambda: CardCommServ._BaseModelWithId__get_next_id())
    dtCreate: datetime.datetime


class CardAT(BaseModelWithId):
    cardATId: str = Field(default_factory=lambda: CardAT._BaseModelWithId__get_next_id())
    dtCreate: datetime.datetime
    strInjurySuspect: str = None
