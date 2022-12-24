from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .test import Test  # noqa: F401


class Table(Base):
    id: int = Column(Integer, primary_key=True, index=True)
    digits = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner: "User" = relationship("User", back_populates="tables")
    test: "Test" = relationship("Test", back_populates="table")
