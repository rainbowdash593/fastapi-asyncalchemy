migrate:
	alembic upgrade head

migration.create:
	alembic revision --message="$(name)"

migration.generate:
	alembic revision --message="$(name)" --autogenerate