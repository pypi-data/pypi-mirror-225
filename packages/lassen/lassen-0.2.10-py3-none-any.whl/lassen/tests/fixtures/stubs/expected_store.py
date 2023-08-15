from sqlalchemy.orm import Mapped, mapped_column
from MOCKED_PACKAGE import NoneType
from MOCKED_PACKAGE import SimpleEnum
from MOCKED_PACKAGE import Union
from MOCKED_PACKAGE import datetime
from MOCKED_PACKAGE import str
from lassen.db.base_class import Base
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql.sqltypes import Enum
from sqlalchemy.sql.sqltypes import String

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import timezone


class UserStub(Base):
    __tablename__ = 'user_stub'

    first_name: Mapped[str]

    last_name: Mapped[Union[str, None]]

    password: Mapped[str]

    enum_value: Mapped[SimpleEnum] = mapped_column(Enum(SimpleEnum))

    creation_date: Mapped[datetime] = mapped_column(DateTime(), default=lambda: datetime.now())

    forward_reference_value: Mapped['timezone'] = mapped_column('timezone')
