from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base_class import Base


if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .table import Test  # noqa: F401


class Attempt(Base):
    id: int = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("test.id"), primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    created = Column(DateTime(timezone=True), server_default=func.now())
    owner: "User" = relationship("User", back_populates="attempts")
    test: "Test" = relationship("Test", back_populates="attempt")
