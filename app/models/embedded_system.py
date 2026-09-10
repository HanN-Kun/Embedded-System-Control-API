import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
from sqlalchemy.orm import relationship

class EmbeddedSystem(Base):
    __tablename__ = 'embedded_systems'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    system_name = Column(String)
    system_uid = Column(String, unique=True)
    api_key = Column(String, unique=True)
    created_at = Column(DateTime)

    owner = relationship("User", back_populates="owned_systems")
    components = relationship("Component", back_populates="embedded_system")
    device_accesses = relationship("DeviceAccess", back_populates="embedded_system")
    device_status = relationship("DeviceStatus", back_populates="embedded_system", uselist=False)
    user_roles = relationship("UserRole", back_populates="embedded_system")

