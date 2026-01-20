from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum

from .lifecycle import ContractStatus


# --------------------
# Blueprint Schemas
# --------------------

class BlueprintFieldCreate(BaseModel):
    field_type: str = Field(..., examples=["text", "date", "signature", "checkbox"])
    label: str
    position_x: int
    position_y: int


class BlueprintCreate(BaseModel):
    name: str
    fields: List[BlueprintFieldCreate]


class BlueprintFieldResponse(BaseModel):
    id: str
    field_type: str
    label: str
    position_x: int
    position_y: int

    class Config:
        from_attributes = True


class BlueprintResponse(BaseModel):
    id: str
    name: str
    fields: List[BlueprintFieldResponse]

    class Config:
        from_attributes = True


# --------------------
# Contract Schemas
# --------------------

class ContractCreate(BaseModel):
    name: str
    blueprint_id: str


class ContractFieldResponse(BaseModel):
    id: str
    field_type: str
    label: str
    position_x: int
    position_y: int
    value: Optional[str]

    class Config:
        from_attributes = True


class ContractResponse(BaseModel):
    id: str
    name: str
    blueprint_id: str
    status: ContractStatus
    fields: List[ContractFieldResponse]

    class Config:
        from_attributes = True


class ContractTransitionRequest(BaseModel):
    to_status: ContractStatus
