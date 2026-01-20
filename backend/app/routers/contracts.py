from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import SessionLocal
from .. import models, schemas
from ..lifecycle import ContractStatus, validate_transition
from typing import Optional
from sqlalchemy.orm import joinedload


router = APIRouter(prefix="/contracts", tags=["Contracts"])


# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.ContractResponse)
def create_contract(
    payload: schemas.ContractCreate,
    db: Session = Depends(get_db),
):
    blueprint = db.query(models.Blueprint).filter(
        models.Blueprint.id == payload.blueprint_id
    ).first()

    if not blueprint:
        raise HTTPException(status_code=404, detail="Blueprint not found")

    contract = models.Contract(
        name=payload.name,
        blueprint_id=blueprint.id,
        status=ContractStatus.CREATED,
    )
    db.add(contract)
    db.flush()  # get contract.id

    # Copy blueprint fields → contract fields
    for field in blueprint.fields:
        contract_field = models.ContractField(
            contract_id=contract.id,
            field_type=field.field_type,
            label=field.label,
            position_x=field.position_x,
            position_y=field.position_y,
        )
        db.add(contract_field)

    db.commit()
    db.refresh(contract)
    return contract
@router.post("/{contract_id}/transition", response_model=schemas.ContractResponse)
def transition_contract(
    contract_id: str,
    payload: schemas.ContractTransitionRequest,
    db: Session = Depends(get_db),
):
    contract = db.query(models.Contract).filter(
        models.Contract.id == contract_id
    ).first()

    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    # Terminal states
    if contract.status in (ContractStatus.LOCKED, ContractStatus.REVOKED):
        raise HTTPException(
            status_code=400,
            detail=f"Contract is {contract.status} and cannot be changed",
        )

    # Validate lifecycle transition
    if not validate_transition(contract.status, payload.to_status):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid transition from {contract.status} to {payload.to_status}",
        )

    contract.status = payload.to_status
    db.commit()
    db.refresh(contract)
    return contract



@router.get("/", response_model=list[schemas.ContractResponse])
def list_contracts(
    group: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Contract).options(
        joinedload(models.Contract.fields)
    )

    if group:
        group = group.lower()

        if group == "active":
            query = query.filter(
                models.Contract.status.in_([
                    ContractStatus.CREATED,
                    ContractStatus.APPROVED,
                    ContractStatus.SENT,
                ])
            )
        elif group == "pending":
            query = query.filter(
                models.Contract.status.in_([
                    ContractStatus.CREATED,
                    ContractStatus.APPROVED,
                ])
            )
        elif group == "signed":
            query = query.filter(
                models.Contract.status.in_([
                    ContractStatus.SIGNED,
                    ContractStatus.LOCKED,
                ])
            )
        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid group filter",
            )

    return query.all()

