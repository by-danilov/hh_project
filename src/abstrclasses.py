from abc import ABC, abstractmethod


class AbstractAPI(ABC):
    """
    Абстрактный класс для работы с API сервиса с вакансиями.
    """

    @abstractmethod
    def get_vacancies(self, search_query: str) -> list:
        """
        Получает вакансии по заданному поисковому запросу.
        """
        pass


class AbstractFileSaver(ABC):
    """
    Абстрактный класс для сохранения и получения данных из файлов.
    """

    @abstractmethod
    def add_vacancy(self, vacancy: 'Vacancy'):
        """
        Добавляет вакансию в файл.
        """
        pass

    @abstractmethod
    def get_vacancies(self, **kwargs) -> list:
        """
        Получает список вакансий из файла по заданным критериям.
        """
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: 'Vacancy'):
        """
        Удаляет вакансию из файла.
        """
        pass
