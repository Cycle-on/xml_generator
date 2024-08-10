import datetime
from typing import ClassVar

from pydantic import BaseModel, Field

from schemas.string_schemas import IncidentType


class FireDepartment(BaseModel):
    dtCreate: datetime.datetime
    strIncidentType: IncidentType
    strObject: str
    bObjectGasified: bool


class Police(BaseModel):
    dtCreate: datetime.datetime


class Ambulance(BaseModel):
    dtCreate: datetime.datetime


class GasDepartment(BaseModel):
    dtCreate: datetime.datetime


class HouseDepartment(BaseModel):
    dtCreate: datetime.datetime


class AntiTerror(BaseModel):
    dtCreate: datetime.datetime
    strInjurySuspect: str = None
