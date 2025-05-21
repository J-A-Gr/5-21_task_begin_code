1. pip install alembic
2. alembic init migrations - sukuriame alembic konfiguracijos faila
3. alembic revision -m "Add new table" - Sukuriame migracija
4. alembic revision --autogenerate -m "Initial migration"
5. alembic upgrade head - paleidziame migracija
