from abc import ABC, abstractmethod


class AbstractParsingVacancy(ABC):
    def __init__(self, query_vacancies: str, area: int, page_limit: int):
        self.query_vacancies: str = query_vacancies
        self.area: int = area
        self.page_limit: int = page_limit
        self.vacancies: list[dict] = []

    def __repr__(self):
        return f'Vacancy for: {self.query_vacancies}'

    @abstractmethod
    def build_url_and_headers(self):
        """
        Prepare url and query_params for parsing
        :return: query_url and query_params
        """
        pass

    @abstractmethod
    def pars_vacancies(self):
        pass


class HHParsingVacancy(AbstractParsingVacancy):
    def __init__(self, query_vacancies: str, area: int, page_limit: int):
        super().__init__(query_vacancies, area, page_limit)
        self.query_url: str = ''
        self.query_params: dict = {}
        self.build_url_and_headers()

    def build_url_and_headers(self):
        self.query_url = f"https://api.hh.ru/vacancies"
        self.query_params = {
            "text": self.query_vacancies,
            "area": self.area,
            "per_page": self.page_limit,
        }

    # def pars_vacancies(self):
    #     vacancies_response = []
    #     async with session.get(url, params=keys_response) as response:
    #         if response.status == 200:
    #             return await response.json()  # Возвращаем данные, если запрос успешен
    #         else:
    #             print(f"Failed to retrieve vacancies from {url}. Status code: {response.status}")


class HabrParsingVacancy(AbstractParsingVacancy):
    def __init__(self, query_vacancies: str, area: int, page_limit: int):
        super().__init__(query_vacancies, area, page_limit)
        self.query_url: str = ''
        self.query_params: dict = {}
        self.build_url_and_headers()

    def build_url_and_headers(self):
        self.query_url = "https://career.habr.com/vacancies?q=" + self.query_vacancies
        self.query_params = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
