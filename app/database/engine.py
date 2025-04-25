from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.database.config import settings

engine = create_engine(
    url=settings.SQLALCHEMY_DATABASE_URI,
    echo=True,
    pool_size=5,
    max_overflow=10
    )

session_factory = sessionmaker(engine)

class Base(DeclarativeBase):
    pass
