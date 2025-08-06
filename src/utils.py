from typing import List
from src.vacancy_class import Vacancy


def filter_vacancies_by_keywords(vacancies: List[Vacancy], keywords: List[str]) -> List[Vacancy]:
    """
    Фильтрует список вакансий по заданным ключевым словам.

    :param vacancies: Список объектов Vacancy.
    :param keywords: Список ключевых слов для поиска.
    :return: Отфильтрованный список объектов Vacancy.
    """
    if not keywords:
        return vacancies

    filtered_vacancies = []
    for vacancy in vacancies:
        for keyword in keywords:
            if keyword.lower() in vacancy.name.lower() or \
                    (vacancy.description and keyword.lower() in vacancy.description.lower()):
                filtered_vacancies.append(vacancy)
                break
    return filtered_vacancies

def filter_vacancies_by_salary(vacancies: List[Vacancy], min_salary: int, max_salary: int) -> List[Vacancy]:
    """
    Фильтрует список вакансий по заданному диапазону зарплат.

    :param vacancies: Список объектов Vacancy.
    :param min_salary: Минимальное значение зарплаты.
    :param max_salary: Максимальное значение зарплаты.
    :return: Отфильтрованный список объектов Vacancy.
    """
    filtered_vacancies = []
    for vacancy in vacancies:
        # Учитываем, что у вакансии может быть указана только salary_from или salary_to
        if (min_salary <= vacancy.salary_from <= max_salary) or \
                (min_salary <= vacancy.salary_to <= max_salary) or \
                (min_salary <= vacancy.salary_from and vacancy.salary_to == 0 and vacancy.salary_from <= max_salary) or \
                (vacancy.salary_from == 0 and vacancy.salary_to <= max_salary):
            filtered_vacancies.append(vacancy)

    return filtered_vacancies
