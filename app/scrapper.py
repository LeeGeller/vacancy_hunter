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
        A method that subclasses must implement to construct the necessary
        URL and headers for a specific purpose. This is a required part of objects
        subclassing this abstract class and must return a combination of URL and
        headers formatted as defined.

        The implementation details depend on the specific use case of the subclass,
        and this function defines the contract that ensures consistent behavior
        and expected structure for generating URLs and headers.

        :raises NotImplementedError: This method must be implemented by the subclass
            and cannot be invoked from the base abstract class.

        :return: A combination of a constructed URL and relevant headers
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
                    data = await response.json()
                    vacancies_list: list[dict] = data.get('items', [])
                    for vacancy in vacancies_list:
                        salary = vacancy.get('salary', {})
                        salary_from = salary.get('from', 0)
                        salary_to = salary.get('to', 0)

                        yield {
                            'Вакансия': vacancy.get('name', 'No title'),
                            'Компания': vacancy.get('employer', {}).get('name', None),
                            'Локация': vacancy.get('area', {}).get('name', None),
                            'Описание': vacancy.get('snippet', {}).get('responsibility', None),
                            'Ссылка': vacancy.get('alternate_url', None),
                            'Опыт работы': vacancy.get('experience', {}).get('name', None),
                            'Зарплата от': salary_from,
                            'Зарплата до': salary_to,
                        }
                    else:
                        print(f"Failed to retrieve vacancies from {self.query_url}. Status code: {response.status}")

    class HabrParsingVacancy(AbstractParsingVacancy):
        def __init__(self, query_vacancies: str, area: int, page_limit: int):
            super().__init__(query_vacancies, area, page_limit)
            self.query_url: str = ''
            self.query_params: dict = {}
            self.build_url_and_headers()

        def build_url_and_headers(self):
            self.query_url: str = "https://career.habr.com/vacancies?q=" + self.query_vacancies
            self.query_params: dict = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }

        @clean_salary
        async def pars_vacancies(self):
            async with aiohttp.ClientSession() as session:
                async with session.get(self.query_url, headers=self.query_params) as response:
                    if response.status == 200:
                        soup = BeautifulSoup(await response.text(), "html.parser")
                        items = soup.find_all("div", class_="vacancy-card__inner")
                        for item in items:
                            title_elem = item.find("a", class_="vacancy-card__title-link")
                            link = "https://career.habr.com" + title_elem['href'] if title_elem else "No link"

                            yield {
                                "Вакансия": title_elem.text.strip() if title_elem else "No title",
                                "Компания": item.find("a", class_="vacancy-card__company-title").text.strip(),
                                "Локация": item.find("span", class_="link-comp--appearance-dark").text.strip(),
                                "Описание": item.find("div", class_="vacancy-card__description").text.strip(),
                                "Ссылка": link,
                                "Зарплата": item.find("div", class_="basic-salary").text.strip() if item.find("div",
                                                                                                              class_="basic-salary") else None,
                                "Опыт работы": "На хабре не указано"
                            }
                        else:
                            print(f"Failed Habr with status: {response.status}")

