import uuid
from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class UserRole(Base):
    __tablename__ = 'user_roles'
    __table_args__ = (
        UniqueConstraint('user_id', 'embedded_system_id', 'role_id', name='uq_user_system_role'),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    embedded_system_id = Column(UUID(as_uuid=True), ForeignKey('embedded_systems.id'), nullable=True)
    role_id = Column(UUID(as_uuid=True), ForeignKey('roles.id'), nullable=False)

    user = relationship("User", back_populates="user_roles")
    embedded_system = relationship("EmbeddedSystem", back_populates="user_roles")
    role = relationship("Role", back_populates="user_roles")