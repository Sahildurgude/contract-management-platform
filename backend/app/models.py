import uuid
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base
from .lifecycle import ContractStatus


def generate_uuid():
    return str(uuid.uuid4())


# --------------------
# Blueprint Models
# --------------------

class Blueprint(Base):
    __tablename__ = "blueprints"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    fields = relationship(
        "BlueprintField",
        back_populates="blueprint",
        cascade="all, delete-orphan",
    )


class BlueprintField(Base):
    __tablename__ = "blueprint_fields"

    id = Column(String, primary_key=True, default=generate_uuid)
    blueprint_id = Column(String, ForeignKey("blueprints.id"), nullable=False)

    field_type = Column(String, nullable=False)  # text | date | signature | checkbox
    label = Column(String, nullable=False)
    position_x = Column(Integer, nullable=False)
    position_y = Column(Integer, nullable=False)

    blueprint = relationship("Blueprint", back_populates="fields")


# --------------------
# Contract Models
# --------------------

class Contract(Base):
    __tablename__ = "contracts"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)

    blueprint_id = Column(String, ForeignKey("blueprints.id"), nullable=False)
    status = Column(
        Enum(ContractStatus),
        nullable=False,
        default=ContractStatus.CREATED,
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    fields = relationship(
        "ContractField",
        back_populates="contract",
        cascade="all, delete-orphan",
    )


class ContractField(Base):
    __tablename__ = "contract_fields"

    id = Column(String, primary_key=True, default=generate_uuid)
    contract_id = Column(String, ForeignKey("contracts.id"), nullable=False)

    field_type = Column(String, nullable=False)
    label = Column(String, nullable=False)
    position_x = Column(Integer, nullable=False)
    position_y = Column(Integer, nullable=False)

    value = Column(Text, nullable=True)

    contract = relationship("Contract", back_populates="fields")
