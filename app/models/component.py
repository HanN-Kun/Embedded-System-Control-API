import uuid
from sqlalchemy import Column,String,ForeignKey,DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
from sqlalchemy.orm import relationship

class Component(Base):
    __tablename__= 'components'

    id= Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4())
    embedded_system_id = Column(UUID(as_uuid=True), ForeignKey('embedded_systems.id'), nullable=False)
    component_name=Column(String)
    component_type=Column(String)
    model= Column(String)
    installed_at=Column(DateTime)
    status=Column(String)

    embedded_system = relationship("EmbeddedSystem", back_populates="components")
    sensors = relationship("Sensor", back_populates="component")


