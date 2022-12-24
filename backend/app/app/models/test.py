from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base_class import Base


if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .table import Table  # noqa: F401
    from .attempt import Attempt  # noqa: F401


class Test(Base):
    id: int = Column(Integer, primary_key=True, index=True)
    errors = Column(String)
    choosed_number = Column(String)
    time: int = Column(Integer)
    owner_id = Column(Integer, ForeignKey("user.id"))
    created = Column(DateTime(timezone=True), server_default=func.now())
    table_id = Column(Integer, ForeignKey("table.id"))
    owner: "User" = relationship("User", back_populates="tests")
    table: "Table" = relationship("Table", back_populates="test")
    attempt: "Attempt" = relationship("Attempt", back_populates="test")
