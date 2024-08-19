from typing import ClassVar

from pydantic import BaseModel
import uuid


class BaseModelWithId(BaseModel):
    """
    BaseModel from pydantic, just with id for every inherited class
    simple example:
         ClassNameId: str = Field(default_factory=lambda: ClassName._BaseModelWithId__get_next_id())
    """

    __id_counter: ClassVar[int] = 0

    @classmethod
    def __get_next_id(cls):
        cls.__id_counter += 1
        return str(uuid.uuid4())
