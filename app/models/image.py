from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, intpk, str100


class Images(Base):
    __tablename__ = "image"

    image_id: Mapped[intpk]
    created_date =  mapped_column(DateTime)
    task_id : Mapped[int]
    file_location: Mapped[str100 | None]
    file_name: Mapped[str100 | None]
    