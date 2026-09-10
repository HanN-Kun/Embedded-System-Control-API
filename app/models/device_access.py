import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
from sqlalchemy.orm import relationship

class DeviceAccess(Base):
    __tablename__ = 'device_access'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    embedded_system_id = Column(UUID(as_uuid=True), ForeignKey('embedded_systems.id'), nullable=False)
    access_level = Column(String)
    granted_at = Column(DateTime)

    user = relationship("User", back_populates="device_accesses")
    embedded_system = relationship("EmbeddedSystem", back_populates="device_accesses")


















