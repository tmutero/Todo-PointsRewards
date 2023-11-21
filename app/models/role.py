from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, intpk, str100


class Role(Base):
    __tablename__ = "role"

    id: Mapped[intpk]
    name: Mapped[str100 | None]

