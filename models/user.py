from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Model(DeclarativeBase):
   pass

class UserOrm(Model):
   __tablename__ = "users"
   id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
   tg_id: Mapped[str] = mapped_column(unique=True)
   datetime_register: Mapped[datetime]
   is_admin: Mapped[bool] = mapped_column(default=False)
   is_staff: Mapped[bool] = mapped_column(default=False)