from sqlalchemy import Column, Integer, String, Text
from app.database.engine import Base


class Vacancy(Base):
    __tablename__ = "vacancies"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    city = Column(String(255))
    description = Column(Text)
    work_format = Column(String(255))
    salary_from = Column(Integer)
    salary_to = Column(Integer)
    currency = Column(String(20))
    url = Column(String)
