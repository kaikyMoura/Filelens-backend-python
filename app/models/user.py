from sqlalchemy import UUID, Column, DateTime, Integer, String, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    name = Column(String, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, index=True)
    role = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
        }
