import requests


class ParsingVacancy:
    def __init__(self, url: str, query_vacancies_list: list[str], area: int, page_limit: int):
        self.url = url
        self.query_vacancies_list = query_vacancies_list
        self.area = area
        self.page_limit = page_limit

    def __repr__(self):
        return f'Vacancy from: {self.url}'

    def check_url(self, url):


    def pars_url(self):

        response = requests.get(self.url)

        keys_response = {
            "text": " ".join(self.query_vacancies_list),
            "area": self.area,
            "per_page": 100,
        }

        vacancies = []
