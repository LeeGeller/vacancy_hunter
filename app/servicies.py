import re


async def clean_salary(salary: str) -> tuple[int, int]:
    """
    The method to process and extract salary details from a list of job vacancies fetched
    via the decorated asynchronous function. The salary range is extracted from the
    string representation in the "Зарплата" field and added as separate fields
    ("Зарплата от" and "Зарплата до") in each vacancy dictionary. The "Зарплата"
    field itself is not modified.

    :param salary: String with salary from habrcarier

    :return: tuple with salary_from and salary_to
    """
    salary_from = 0
    salary_to = 0

    if salary is not None:
        salary_numbers = re.findall(r"\d+", salary.replace(" ", ""))

        if "до" in salary and salary_numbers:
            salary_to = int(salary_numbers[-1])
        if "от" in salary and salary_numbers:
            salary_from = int(salary_numbers[0])

        salary_to = salary_from if salary_to < salary_from else salary_to

    return int(salary_from), int(salary_to)


async def make_vacancy(
        name,
        company,
        location,
        description,
        url,
        salary_from,
        salary_to,
        currency,
        experience,
        work_format,
):
    return {
        "Вакансия": name,
        "Компания": company,
        "Локация": location,
        "Описание": description,
        "Ссылка": url,
        "Опыт работы": experience,
        "Зарплата от": salary_from or 0,
        "Зарплата до": salary_to or 0,
        "Валюта": currency,
        "Формат работы": work_format,
    }


async def clean_vacancies_list(vacancies: list):
    clean_vacancy_list = []
    for vacancy in vacancies:
        name = vacancy.get("name", "No title")
        company = vacancy.get("employer", {}).get("name", None)
        location = vacancy.get("area", {}).get("name", None)
        description = vacancy.get("snippet", {}).get("responsibility", None)
        url = vacancy.get("alternate_url", None)

        salary = vacancy.get("salary", {})
        salary_from = salary.get("from", 0)
        salary_to = salary.get("to", 0)
        currency = salary.get("currency")
        experience = vacancy.get("experience", {}).get("name", None)
        work_format = vacancy.get("work_format")

        clean_vacancy = await make_vacancy(
            name,
            company,
            location,
            description,
            url,
            salary_from or 0,
            salary_to or 0,
            currency,
            experience,
            work_format.get("name"),
        )
        clean_vacancy_list.extend(clean_vacancy)
    return clean_vacancy_list
