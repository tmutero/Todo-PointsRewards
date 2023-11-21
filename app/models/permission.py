from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, intpk, str100


class Permission(Base):
    __tablename__ = "permission"

    permission_id: Mapped[intpk]
    user_id :  Mapped[int]
    role_id : Mapped[int]

