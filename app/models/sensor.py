import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
from sqlalchemy.orm import relationship

class Sensor(Base):
    __tablename__ = 'sensors'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    component_id = Column(UUID(as_uuid=True), ForeignKey('components.id'), nullable=False)
    sensor_name = Column(String)
    sensor_type = Column(String)
    unit = Column(String)

    component = relationship("Component", back_populates="sensors")
    readings = relationship("SensorReading", back_populates="sensor")



