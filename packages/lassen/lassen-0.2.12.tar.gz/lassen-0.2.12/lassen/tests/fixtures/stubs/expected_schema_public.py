from pydantic import BaseModel, Field, Extra
from MOCKED_PACKAGE import NoneType
from MOCKED_PACKAGE import Union
from MOCKED_PACKAGE import str

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import timezone


# Shared properties
class UserStubBase(BaseModel):
    class Config:
        extra = Extra.forbid


# STORE: SEARCH FILTER PROPERTIES
class UserStubFilter(UserStubBase):

    pass



# API/STORE: CREATE PROPERTIES
class UserStubCreate(UserStubBase):

    password: str



# API/STORE: UPDATE PROPERTIES
class UserStubUpdate(UserStubBase):

    pass



# API/STORE: RETRIEVE PROPERTIES
class UserStub(UserStubBase):

    first_name: str = Field(description='First name of the user', examples=['John'])

    last_name: Union[str, None] = Field(description='Last name of the user', examples=['Smith'])

    password: str


    class Config:
        orm_mode = True