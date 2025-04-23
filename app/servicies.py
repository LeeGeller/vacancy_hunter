import re
from functools import wraps


def clean_salary_from_habr(func):
    """
    Decorator to process and extract salary details from a list of job vacancies fetched
    via the decorated asynchronous function. The salary range is extracted from the
    string representation in the "Зарплата" field and added as separate fields
    ("Зарплата от" and "Зарплата до") in each vacancy dictionary. The "Зарплата"
    field itself is not modified.

    The function expects that the decorated function returns an awaitable list of
    vacancy dictionaries. If the salary contains textual indicators ('до' for
    upper limit and 'от' for lower limit), only the relevant numbers from the string
    will be parsed into integers.

    :param func: Asynchronous function that returns a list of job vacancies,
        where each job vacancy is represented as a dictionary with at least a
        "Зарплата" field.

    :return: A wrapper function that processes the salary data and returns
        the same list of job vacancies with added salary fields ("Зарплата от",
        "Зарплата до").
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        vacancies = await func(*args, **kwargs)

        for vacancy in vacancies:
            salary: str = vacancy.get("Зарплата", "")
            salary_from = 0
            salary_to = 0

            salary_numbers: list[str] = re.findall(r'\d+', salary.replace(' ', ''))

            if 'до' in salary and salary_numbers:
                salary_to = int(salary_numbers[-1])
            if 'от' in salary and salary_numbers:
                salary_from = int(salary_numbers[0])

            salary_to = salary_from if salary_to < salary_from else salary_to

            vacancy["Зарплата от"]: int = salary_from
            vacancy["Зарплата до"]: int = salary_to

        return vacancies

    return wrapper
