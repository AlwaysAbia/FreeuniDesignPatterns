from typing import List
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from uuid import UUID

from DPAssignment2.src.db.database import Database
from DPAssignment2.src.db.repository.unit_repository import UnitRepository
from DPAssignment2.src.service.unit_service import UnitService


# Pydantic models for request/response
class UnitCreate(BaseModel):
    name: str

class Unit(BaseModel):
    id: UUID
    name: str

class UnitResponse(BaseModel):
    unit: Unit

class UnitsResponse(BaseModel):
    units: List[Unit]

class ErrorResponse(BaseModel):
    error: dict

# Create router
router = APIRouter(
    prefix="/units",
    tags=["units"]
)

# Database dependency
def get_db():
    db = Database()
    db.connect()
    try:
        yield db
    finally:
        db.disconnect()

# Service dependency
def get_unit_service(db: Database = Depends(get_db)) -> UnitService:
    return UnitService(UnitRepository(db))

@router.post("", response_model=UnitResponse, status_code=201, responses={409: {"model": ErrorResponse}})
async def create_unit(unit_data: UnitCreate, service: UnitService = Depends(get_unit_service)):
    try:
        unit = service.create_unit(unit_data.name)
        # Convert domain model to Pydantic model
        return {"unit": Unit(id=unit.id, name=unit.name)}
    except ValueError as e:
        raise HTTPException(status_code=409, detail={"message": str(e)})

@router.get("/{unit_id}", response_model=UnitResponse, responses={404: {"model": ErrorResponse}})
async def get_unit(unit_id: UUID, service: UnitService = Depends(get_unit_service)):
    unit = service.read_unit(unit_id)
    if unit is None:
        raise HTTPException(
            status_code=404,
            detail={"message": f"Unit with id<{unit_id}> does not exist."}
        )
    return {"unit": Unit(id=unit.id, name=unit.name)}

@router.get("", response_model=UnitsResponse)
async def list_units(service: UnitService = Depends(get_unit_service)):
    units = service.list_units()
    # Convert domain models to Pydantic models
    return {"units": [Unit(id=unit.id, name=unit.name) for unit in units]}