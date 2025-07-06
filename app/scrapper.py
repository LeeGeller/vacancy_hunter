import asyncio
from abc import ABC, abstractmethod
import aiohttp
from bs4 import BeautifulSoup
from app.servicies import clean_salary, clean_vacancies_list
import urllib.parse


class AbstractURLBuilder(ABC):

    @abstractmethod
    def build_url(self) -> str:
        pass

    @abstractmethod
    def build_params(self) -> dict:
        pass

    @abstractmethod
    def build_headers(self) -> dict:
        pass


class AbstractParsVacancies(ABC):

    @abstractmethod
    async def pars_vacancies(self):
        """ :return: generator vacancies list"""
        pass
