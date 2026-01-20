from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import SessionLocal
from .. import models, schemas

router = APIRouter(prefix="/blueprints", tags=["Blueprints"])


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.BlueprintResponse)
def create_blueprint(
    payload: schemas.BlueprintCreate,
    db: Session = Depends(get_db),
):
    blueprint = models.Blueprint(name=payload.name)
    db.add(blueprint)
    db.flush()  # get blueprint.id

    for field in payload.fields:
        blueprint_field = models.BlueprintField(
            blueprint_id=blueprint.id,
            field_type=field.field_type,
            label=field.label,
            position_x=field.position_x,
            position_y=field.position_y,
        )
        db.add(blueprint_field)

    db.commit()
    db.refresh(blueprint)
    return blueprint


@router.get("/", response_model=list[schemas.BlueprintResponse])
def list_blueprints(db: Session = Depends(get_db)):
    return db.query(models.Blueprint).all()


@router.get("/{blueprint_id}", response_model=schemas.BlueprintResponse)
def get_blueprint(blueprint_id: str, db: Session = Depends(get_db)):
    blueprint = db.query(models.Blueprint).filter(
        models.Blueprint.id == blueprint_id
    ).first()

    if not blueprint:
        raise HTTPException(status_code=404, detail="Blueprint not found")

    return blueprint
