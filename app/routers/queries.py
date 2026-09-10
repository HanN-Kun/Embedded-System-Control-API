import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.sensor import SensorResponse
from app.services import query_service

router = APIRouter(prefix="/queries", tags=["Relational Queries"])


@router.get("/embedded-systems/{system_id}/sensors", response_model=list[SensorResponse])
def get_sensors_of_system(system_id: uuid.UUID, db: Session = Depends(get_db)):
    return query_service.get_sensors_of_system(db, system_id)


@router.get("/sensors/{sensor_id}/embedded-system")
def get_system_of_sensor(sensor_id: uuid.UUID, db: Session = Depends(get_db)):
    return query_service.get_system_of_sensor(db, sensor_id)


@router.get("/sensors/search", response_model=list[SensorResponse])
def search_sensors_by_name(keyword: str, db: Session = Depends(get_db)):
    return query_service.search_sensors_by_name(db, keyword)


@router.get("/embedded-systems/{system_id}/sensors/search", response_model=list[SensorResponse])
def search_sensors_in_system(system_id: uuid.UUID, keyword: str, db: Session = Depends(get_db)):
    return query_service.search_sensors_in_system(db, system_id, keyword)