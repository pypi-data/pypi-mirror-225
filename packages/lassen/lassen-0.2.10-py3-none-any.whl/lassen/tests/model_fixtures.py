from pydantic import BaseModel
from sqlalchemy import Column, Integer, String

from lassen.db.base_class import Base


class SampleModel(Base):
    __tablename__ = "samplemodel"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class SampleSchemaFilter(BaseModel):
    pass

class SampleSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True


class SampleSchemaCreate(SampleSchema):
    pass

class SampleSchemaUpdate(SampleSchema):
    pass
