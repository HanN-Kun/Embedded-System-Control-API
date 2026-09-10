import uuid
from sqlalchemy import Column, Float, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base

class SensorReading(Base):
    __tablename__ = 'sensor_readings'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sensor_id = Column(UUID(as_uuid=True), ForeignKey('sensors.id'), nullable=False)
    value = Column(Float)
    time_stamp = Column(DateTime)

    sensor = relationship("Sensor", back_populates="readings")