from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from db.config import settings


sync_engine = create_engine(
	url=settings.db_url_psycopg,
	echo=False,
	pool_size=5,
	max_overflow=10,
)

session_factory = sessionmaker(sync_engine)


class Base(DeclarativeBase):

	repr_cols_num = 3
	repr_cols = tuple()

	def __repr__(self):
		cols = []
		for idx, col in enumerate(self.__table__.columns.keys()):
			if col in self.repr_cols or idx < self.repr_cols_num:
				cols.append(f"{col}={getattr(self, col)}")

		return f"<{self.__class__.__name__} {', '.join(cols)}>"
