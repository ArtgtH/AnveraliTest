from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base, sync_engine


class User(Base):
	__tablename__ = 'users'

	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	password: Mapped[str]
	name: Mapped[str] = mapped_column(String(255), unique=True)
	telephone: Mapped[int] = mapped_column(String(11), unique=True)
	experience: Mapped[int] = mapped_column(Integer)
	role: Mapped[str]


if __name__ == '__main__':

	Base.metadata.drop_all(sync_engine)
	Base.metadata.create_all(sync_engine)
