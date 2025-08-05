import requests
from src.abstrclasses import AbstractAPI


class HeadHunterAPI(AbstractAPI):
    """
    Класс для работы с API HeadHunter.
    """
    def __init__(self):
        """
        Инициализация класса.
        """
        self.__base_url = 'https://api.hh.ru/vacancies'
        self.__headers = {
            'HH-User-Agent': 'HH-Project-Parser/1.0'
        }

    def __check_api_connection(self):
        """
        Приватный метод для проверки соединения с API.
        """
        response = requests.get(self.__base_url, headers=self.__headers)
        if response.status_code != 200:
            raise ConnectionError(f"Ошибка соединения с API. Код ошибки: {response.status_code}")
        print("Соединение с API hh.ru успешно установлено.")

    def get_vacancies(self, search_query: str) -> list:
        """
        Получает вакансии с hh.ru по заданному поисковому запросу.
        :param search_query: Поисковый запрос (например, "Python").
        :return: Список вакансий в виде словарей.
        """
        self.__check_api_connection()
        all_vacancies = []
        page = 0
        pages = 1  # Начальное значение для цикла

        while page < pages and page < 3:
            params = {
                'text': search_query,
                'per_page': 100,
                'page': page,
                'area': 113,  # Код для России
                'search_field': 'name'  # Добавляем параметр для поиска только по названию
            }
            try:
                response = requests.get(self.__base_url, headers=self.__headers, params=params)
                response.raise_for_status()
                data = response.json()
                all_vacancies.extend(data['items'])
                pages = data['pages']
                page += 1
                print(f"Обработана страница {page} из {pages}.")
            except requests.exceptions.RequestException as e:
                print(f"Ошибка при запросе к API: {e}")
                break

        return all_vacancies
