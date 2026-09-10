import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
from sqlalchemy.orm import relationship

class DeviceStatus(Base):
    __tablename__ = 'device_status'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    embedded_system_id = Column(UUID(as_uuid=True), ForeignKey('embedded_systems.id'), unique=True, nullable=False)
    is_online = Column(Boolean)
    last_seen = Column(DateTime)
    ip_address = Column(String)

    embedded_system = relationship("EmbeddedSystem", back_populates="device_status")




