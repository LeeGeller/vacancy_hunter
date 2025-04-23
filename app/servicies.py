import re
from functools import wraps


def clean_salary_from_habr(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        vacancies = await func(*args, **kwargs)

        for vacancy in vacancies:
            salary = vacancy.get("Зарплата", "")
            salary_from = 0
            salary_to = 0

            salary_numbers = re.findall(r'\d+', salary.replace(' ', ''))

            if 'до' in salary and salary_numbers:
                salary_to = int(salary_numbers[-1])
            if 'от' in salary and salary_numbers:
                salary_from = int(salary_numbers[0])

            salary_to = salary_from if salary_to < salary_from else salary_to

            vacancy["Зарплата от"] = salary_from
            vacancy["Зарплата до"] = salary_to

        return vacancies
    return wrapper
