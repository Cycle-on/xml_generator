from typing import ClassVar

from pydantic import BaseModel, Field


class BaseModelWithId(BaseModel):
    """
    BaseModel from pydantic, just with id counter for every inherited class
    simple example:
         ClassNameId: str = Field(default_factory=lambda: ClassNameId._BaseModelWithId__get_next_id())
    """

    __id_counter: ClassVar[int] = 0

    @classmethod
    def __get_next_id(cls):
        cls.__id_counter += 1
        return str(cls.__id_counter)


"""class C1(BaseModelWithId):
    id: str = Field(default_factory=lambda: C1._BaseModelWithId__get_next_id())
    a1: int
    a2: str


class C2(BaseModelWithId):
    id: str = Field(default_factory=lambda: C2._BaseModelWithId__get_next_id())


c1_1 = C1(a1=1, a2='mew')
c1_2 = C1(a1=1, a2='str')
c2_1 = C2()
c2_2 = C2()
print(c1_1.id, c2_2.id, c2_1.id, c2_2.id)
"""
