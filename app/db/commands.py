from sqlalchemy import select

from db.database import session_factory

from db.models import User


class ORMCommands:
	@staticmethod
	def get_all():
		with session_factory() as session:
			query = select(User)
			result = session.execute(query)
			return result.fetchall()

	@staticmethod
	def register_new_user(user):
		with session_factory() as session:
			new_user = User(password=user.password, name=user.name, telephone=user.telephone, experience=user.experience, role=user.role)
			session.add(new_user)
			session.flush()
			print(new_user)
			session.commit()

	@staticmethod
	def login_user(username):
		with session_factory() as session:
			user = session.query(User).filter_by(name=username).first()
			if user:
				return user
			return False

	@staticmethod
	def get_all_implementers():
		with session_factory() as session:
			query = select(User).where(User.role == 'implementer')
			result = session.execute(query)
			return result.scalars().all()

	@staticmethod
	def get_all_consumers():
		with session_factory() as session:
			query = select(User).where(User.role == 'consumer')
			result = session.execute(query)
			return result.scalars().all()

	@staticmethod
	def get_one_user(idx: int):
		with session_factory() as session:
			query = select(User).where(User.id == int(idx))
			result = session.execute(query)
			return result.scalar()

	@staticmethod
	def delete_user(idx: int):
		with session_factory() as session:
			user = session.query(User).filter(User.id == int(idx)).one()
			session.delete(user)
			session.commit()


if __name__ == '__main__':
	print(ORMCommands.get_all())

