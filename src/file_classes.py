import json
import os
from typing import Any
from src.abstrclasses import AbstractFileSaver
from src.vacancy_class import Vacancy


class JSONSaver(AbstractFileSaver):
    """
    Класс для сохранения и работы с данными о вакансиях в JSON-файле.
    """

    def __init__(self, filename: str = 'data/vacancies.json'):
        """
        Инициализация класса.
        :param filename: Имя файла для сохранения данных.
        """
        self.__filename = filename
        self.__create_file_if_not_exists()

    def __create_file_if_not_exists(self):
        """
        Приватный метод для создания файла, если он не существует.
        """
        os.makedirs(os.path.dirname(self.__filename), exist_ok=True)
        if not os.path.exists(self.__filename) or os.path.getsize(self.__filename) == 0:
            with open(self.__filename, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def add_vacancy(self, vacancy: Vacancy):
        """
        Добавляет вакансию в файл.
        """
        vacancies = self.get_vacancies()
        vacancy_dict = {
            'name': vacancy.name,
            'url': vacancy.url,
            'salary_from': vacancy.salary_from,
            'salary_to': vacancy.salary_to,
            'currency': vacancy.currency,
            'description': vacancy.description
        }

        if vacancy_dict not in vacancies:
            vacancies.append(vacancy_dict)
            with open(self.__filename, 'w', encoding='utf-8') as f:
                json.dump(vacancies, f, ensure_ascii=False, indent=4)
            print(f"Вакансия '{vacancy.name}' успешно добавлена.")
        else:
            print(f"Вакансия '{vacancy.name}' уже существует в файле.")

    def get_vacancies(self, **kwargs: Any) -> list:
        """
        Получает список вакансий из файла по заданным критериям.
        :param kwargs: Критерии фильтрации.
        :return: Список вакансий в виде словарей.
        """
        if not os.path.exists(self.__filename) or os.path.getsize(self.__filename) == 0:
            return []

        with open(self.__filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not kwargs:
            return data

        filtered_vacancies = []
        for vacancy in data:
            match = True
            for key, value in kwargs.items():
                if vacancy.get(key) != value:
                    match = False
                    break
            if match:
                filtered_vacancies.append(vacancy)
        return filtered_vacancies

    def delete_vacancy(self, vacancy_index: int):
        """
        Удаляет вакансию из файла по её индексу.
        """
        vacancies = self.get_vacancies()

        if 0 <= vacancy_index < len(vacancies):
            vacancy_name = vacancies[vacancy_index]['name']
            del vacancies[vacancy_index]
            with open(self.__filename, 'w', encoding='utf-8') as f:
                json.dump(vacancies, f, ensure_ascii=False, indent=4)
            print(f"Вакансия '{vacancy_name}' успешно удалена.")
        else:
            print(f"Некорректный индекс для удаления: {vacancy_index}")

    def clear_vacancies(self):
        """
        Полностью очищает файл с вакансиями.
        """
        with open(self.__filename, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=4)
        print("Все вакансии успешно удалены из файла.")
