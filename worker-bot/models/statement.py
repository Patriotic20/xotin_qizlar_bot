from sqlalchemy import BigInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base, TimestampMixin


class Statement(Base, TimestampMixin):
    __tablename__ = "statements"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    description: Mapped[str] = mapped_column(Text)
    file_id: Mapped[str | None] = mapped_column(String(200), nullable=True)
    file_type: Mapped[str | None] = mapped_column(String(20), nullable=True)
    client_tg_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending", index=True)
    operator_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
