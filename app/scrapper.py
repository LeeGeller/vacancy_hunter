import asyncio
import re
from abc import ABC, abstractmethod
import aiohttp
from bs4 import BeautifulSoup
from typing import Dict, List
from app.servicies import clean_salary, make_vacancy, clean_vacancies_list
import urllib.parse


class AbstractParsingVacancy(ABC):
    def __init__(self, query_vacancies: str, area: int, page_limit: int):
        self.query_vacancies: str = query_vacancies
        self.area: int = area
        self.page_limit: int = page_limit
        self.vacancies: list[dict] = []
        self.query_url = ""
        self.query_params = {}

    @property
    def __repr__(self):
        return f"Vacancy for: {self.query_vacancies}"

    @abstractmethod
    def build_url_and_headers(self):
        """
        A method that must be implemented by subclasses to construct the necessary
        URL and headers for a specific purpose. This is a required part of objects
        subclassing this abstract class and must return a combination of URL and
        headers formatted as defined.

        The implementation details depend on the specific use case of the subclass,
        and this function defines the contract that ensures consistent behavior
        and expected structure for generating URLs and headers.

        :raises NotImplementedError: This method must be implemented by the subclass
            and cannot be invoked from the base abstract class.

        :return: A combination of a constructed URL and relevant headers
        :rtype: None
        """
        pass

    async def pars_vacancies(self):
        """
        An abstract method that serves as a contract for subclasses to implement
        the functionality for parsing vacancies. This method must be overridden
        in any non-abstract subclass.

        The `pars_vacancies` method is intended to encapsulate all necessary
        logic for extracting and processing vacancy data, adhering to the specific
        requirements of the subclass implementation.

        :raises NotImplementedError: If the method is not implemented in a subclass.
        """
        async with aiohttp.ClientSession() as session:
            limit = 0
            while limit < self.page_limit:
                async with session.get(
                    self.query_url, params=self.query_params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.vacancies.extend(data.get("items", []))
                        limit += 1
                        await asyncio.sleep(2)
                    else:
                        print(
                            f"Failed to retrieve vacancies from {self.query_url}. Status code: {response.status}"
                        )
                        break


class HHParsingVacancy(AbstractParsingVacancy):
    def __init__(self, query_vacancies: str, area: int, page_limit: int):
        super().__init__(query_vacancies, area, page_limit)
        self.build_url_and_headers()

    def build_url_and_headers(self):
        self.query_url = f"https://api.hh.ru/vacancies"
        self.query_params = {
            "text": self.query_vacancies,
            "area": self.area,
            "per_page": self.page_limit,
        }

    async def pars_vacancies(self):
        await self.pars_vacancies()
        clean_vacancies = clean_vacancies_list(self.vacancies)
        self.vacancies = clean_vacancies


class HabrParsingVacancy(AbstractParsingVacancy):
    def __init__(self, query_vacancies: str, area: int, page_limit: int):
        super().__init__(query_vacancies, area, page_limit)
        self.build_url_and_headers()

    def build_url_and_headers(self):
        self.query_vacancies = "".join(urllib.parse.quote(self.query_vacancies))
        self.query_url: str = (
            "https://career.habr.com/vacancies?q=" + self.query_vacancies
        )
        self.query_params: dict = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    async def pars_vacancies(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.query_url, headers=self.query_params
            ) as response:
                if response.status == 200:
                    soup = BeautifulSoup(await response.text(), "html.parser")
                    items = soup.find_all(string=re.compile(self.query_vacancies))
                for item in items:
                    title_elem = item.find("a", class_="vacancy-card__title-link")
                    link = (
                        "https://career.habr.com" + title_elem["href"]
                        if title_elem
                        else "No link"
                    )

                    salary_from, salary_to = clean_salary(
                        item.find("div", class_="basic-salary").text.strip()
                    )

                    self.vacancies.append(
                        {
                            "Вакансия": (
                                title_elem.text.strip() if title_elem else "No title"
                            ),
                            "Компания": item.find(
                                "a", class_="vacancy-card__company-title"
                            ).text.strip(),
                            "Локация": item.find(
                                "span", class_="link-comp--appearance-dark"
                            ).text.strip(),
                            "Описание": item.find(
                                "div", class_="vacancy-card__description"
                            ).text.strip(),
                            "Ссылка": link,
                            "Зарплата": (
                                item.find("div", class_="basic-salary").text.strip()
                                if item.find("div", class_="basic-salary")
                                else None
                            ),
                            "Опыт работы": "На хабре не указано",
                        }
                    )
                else:
                    print(f"Failed Habr with status: {response.status}")


async def pars_fabric(
    query_vacancies: str = "Python-developer, python backend",
    area: int = 113,
    page_limit: int = 2,
) -> Dict[str, List[dict]]:
    """
    Asynchronous factory for launching vacancy parsers from multiple websites.

    Creates class instances for each platform, starts them asynchronously,
    and collects the results into a dictionary.

    :param query_vacancies: String containing keywords for vacancy search.
    :param area: Region ID for the vacancy search.
    :param page_limit: Maximum number of pages to parse.
    :return: A dictionary where keys are site names and values are lists of vacancies represented as dictionaries.
    """
    hh_vacancies = HHParsingVacancy(query_vacancies, area, page_limit)
    habr_vacancies = HabrParsingVacancy(query_vacancies, area, page_limit)

    try:
        await hh_vacancies.pars_vacancies()
    except Exception as e:
        print(f"Error parsing HH vacancies: {e}")

    try:
        await habr_vacancies.pars_vacancies()
    except Exception as e:
        print(f"Error parsing Habr vacancies: {e}")

    all_vacancies = {"HH": hh_vacancies.vacancies, "Habr": habr_vacancies.vacancies}

    return all_vacancies


print(asyncio.run(pars_fabric()))
