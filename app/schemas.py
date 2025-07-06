from pydentic import BaseModel


class VacancySerialized(BaseModel):
    id: int
    title: str
    city: str | None
    description: str | None
    work_format: str | None
    salary_from: int | None
    salary_to: int | None
    currency: str | None
    url: str | None

    class Config:
        orm_mode = True
