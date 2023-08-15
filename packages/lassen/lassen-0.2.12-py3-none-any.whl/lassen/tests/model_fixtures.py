from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

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


class SampleChainedParent(Base):
    __tablename__ = "samplechainedparent"
    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey('samplechainedparent.id'), nullable=True)
    identifier = Column(String, index=True)

    # Self-referential relationship
    parent = relationship(
        "SampleChainedParent",
        remote_side=[id],
        back_populates="children"
    )
    children = relationship("SampleChainedParent", back_populates="parent")

class SampleChainedParentFilter(BaseModel):
    pass

class SampleChainedParentBase(BaseModel):
    identifier: str
    parent_id: int | None = None

    class Config:
        orm_mode = True

class SampleChainedParentCreate(SampleChainedParentBase):
    pass

class SampleChainedParentUpdate(SampleChainedParentBase):
    pass


class SampleChainedChild(Base):
    __tablename__ = "samplechainedchild"
    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey('samplechainedparent.id'))
    parent = relationship("SampleChainedParent", backref="child")


class SampleChainedChildFilter(BaseModel):
    pass

class SampleChainedChildBase(BaseModel):
    parent_id: int

    class Config:
        orm_mode = True

class SampleChainedChildCreate(SampleChainedChildBase):
    pass

class SampleChainedChildUpdate(SampleChainedChildBase):
    pass
