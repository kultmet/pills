import asyncio
import json
from datetime import date
from enum import StrEnum
from typing import Annotated, List, Optional

from fastapi import (
    Body,
    Depends,
    HTTPException,
    Path,
    Query,
    Request,
    WebSocket,
    WebSocketDisconnect,
    routing,
    staticfiles,
    status,
    templating,
)
from pydantic import BaseModel, Field
from sqlalchemy import insert
from sqlalchemy.orm import Session

from src.database import get_db
from src.pills.models import BeforeAfterDuringMeals, Drug, Pill, User

pills_router = routing.APIRouter(prefix="", tags=["pills"])


@pills_router.get("/pills")
def get_pills(db: Session = Depends(get_db)):
    return db.query(Pill).all()


class UnitEnum(StrEnum):
    mg = "мг"
    ml = "мл"


class Relation(StrEnum):
    before = "До"
    after = "После"
    with_ = "Во время"


class PillBody(BaseModel):
    name: str = Field()
    dosage: float = Field()
    units: UnitEnum = Field(UnitEnum.mg)
    user_id: int = Field()
    amount: int = Field()
    half: Optional[bool] = Field(False)
    relation: Relation = Field(Relation.with_)
    timedelta: Optional[int] = Field()


@pills_router.post("/pills")
def create_pill(body: Annotated[PillBody, Body()], db: Session = Depends(get_db)):
    drug_id = db.execute(
        insert(Drug)
        .values(name=body.name, dosage=body.dosage, units=body.units)
        .returning(Drug.id)
    ).scalar()
    meal_id = db.execute(
        insert(BeforeAfterDuringMeals)
        .values(relation=body.relation, timedelta=body.timedelta)
        .returning(BeforeAfterDuringMeals.id)
    ).scalar()
    print(drug_id, meal_id)
    db_pill = Pill(
        user_id=body.user_id,
        drug_id=drug_id,
        amount=body.amount,
        half=body.half,
        meal_id=meal_id,
    )
    db.add(db_pill)
    db.commit()
    db.refresh(db_pill)
    return db_pill
