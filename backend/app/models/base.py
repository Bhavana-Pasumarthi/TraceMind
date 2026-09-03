"""
Shared SQLAlchemy declarative base.

All model modules import `Base` from here (not from database.session)
so that Alembic's `env.py` can import `app.models` and get every table
registered on one MetaData object for autogeneration.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
