import unittest
import os
import json
from src.api_classes import HeadHunterAPI
from src.vacancy_class import Vacancy
from src.file_classes import JSONSaver
from src.utils import filter_vacancies_by_keywords


class TestHeadHunterAPI(unittest.TestCase):
    """
    Тестирование класса HeadHunterAPI.
    """

    def setUp(self):
        """
        Подготовка к тестам: создание экземпляра класса.
        """
        self.hh_api = HeadHunterAPI()

    def test_get_vacancies(self):
        """
        Проверка, что метод get_vacancies возвращает непустой список.
        """
        vacancies = self.hh_api.get_vacancies('Python')
        self.assertIsInstance(vacancies, list)
        self.assertGreater(len(vacancies), 0)


# ---
class TestVacancy(unittest.TestCase):
    """
    Тестирование класса Vacancy.
    """

    def setUp(self):
        """
        Подготовка к тестам: создание тестовых данных и экземпляров класса.
        """
        # Данные от API
        self.test_data_api_with_salary = {
            'name': 'Python Developer',
            'alternate_url': 'test_url_1',
            'salary': {'from': 100000, 'to': 150000, 'currency': 'RUR'},
            'snippet': {'requirement': 'Опыт работы от 3 лет.'}
        }
        self.test_data_api_without_salary = {
            'name': 'Junior Python',
            'alternate_url': 'test_url_2',
            'salary': None,
            'snippet': {'requirement': 'Без опыта.'}
        }

        # Данные из JSON-файла
        self.test_data_json_with_salary = {
            'name': 'Python Developer',
            'url': 'test_url_1',
            'salary_from': 100000,
            'salary_to': 150000,
            'currency': 'RUR',
            'description': 'Опыт работы от 3 лет.'
        }

        self.vacancy1_api = Vacancy(self.test_data_api_with_salary)
        self.vacancy2_api = Vacancy(self.test_data_api_without_salary)
        self.vacancy_json = Vacancy(self.test_data_json_with_salary)

    def test_init_from_api_with_salary(self):
        """
        Проверка корректной инициализации вакансии с зарплатой (от API).
        """
        self.assertEqual(self.vacancy1_api.name, 'Python Developer')
        self.assertEqual(self.vacancy1_api.salary_from, 100000)
        self.assertEqual(self.vacancy1_api.salary_to, 150000)
        self.assertEqual(self.vacancy1_api.currency, 'RUR')

    def test_init_from_api_without_salary(self):
        """
        Проверка корректной инициализации вакансии без зарплаты (от API).
        """
        self.assertEqual(self.vacancy2_api.name, 'Junior Python')
        self.assertEqual(self.vacancy2_api.salary_from, 0)
        self.assertEqual(self.vacancy2_api.salary_to, 0)
        self.assertEqual(self.vacancy2_api.currency, 'Зарплата не указана')

    def test_init_from_json(self):
        """
        Проверка корректной инициализации вакансии из JSON-файла.
        """
        self.assertEqual(self.vacancy_json.name, 'Python Developer')
        self.assertEqual(self.vacancy_json.url, 'test_url_1')
        self.assertEqual(self.vacancy_json.salary_from, 100000)

    def test_comparison_methods(self):
        """
        Проверка магических методов сравнения.
        """
        self.assertTrue(self.vacancy1_api > self.vacancy2_api)
        self.assertTrue(self.vacancy2_api < self.vacancy1_api)
        self.assertFalse(self.vacancy1_api == self.vacancy2_api)

    def test_str_representation(self):
        """
        Проверка строкового представления вакансии.
        """
        expected_str = ("Вакансия: Python Developer\n"
                        "Зарплата: 100000 - 150000 RUR\n"
                        "Ссылка: test_url_1\n"
                        "Требования: Опыт работы от 3 лет.\n")
        self.assertEqual(str(self.vacancy1_api), expected_str)


# ---
class TestJSONSaver(unittest.TestCase):
    """
    Тестирование класса JSONSaver.
    """

    def setUp(self):
        """
        Подготовка к тестам: создание временного файла.
        """
        self.test_filename = 'data/test_vacancies.json'
        # Убеждаемся, что директория существует
        os.makedirs(os.path.dirname(self.test_filename), exist_ok=True)
        self.json_saver = JSONSaver(self.test_filename)

        self.test_data = {
            'name': 'Test Vacancy',
            'alternate_url': 'test_url_3',
            'salary': {'from': 50000, 'to': 70000, 'currency': 'RUR'},
            'snippet': {'requirement': 'Тестовые требования.'}
        }
        self.vacancy = Vacancy(self.test_data)

        self.test_data_2 = {
            'name': 'Another Vacancy',
            'alternate_url': 'test_url_4',
            'salary': {'from': 80000, 'to': 100000, 'currency': 'RUR'},
            'snippet': {'requirement': 'Ещё требования.'}
        }
        self.vacancy2 = Vacancy(self.test_data_2)

    def tearDown(self):
        """
        Очистка после тестов: удаление временного файла.
        """
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_add_vacancy(self):
        """
        Проверка добавления вакансии в файл.
        """
        self.json_saver.add_vacancy(self.vacancy)
        with open(self.test_filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]['name'], 'Test Vacancy')

    def test_get_vacancies(self):
        """
        Проверка получения вакансий из файла.
        """
        self.json_saver.add_vacancy(self.vacancy)
        vacancies = self.json_saver.get_vacancies()
        self.assertEqual(len(vacancies), 1)
        # Проверяем, что зарплата сохранена корректно
        self.assertEqual(vacancies[0]['salary_from'], 50000)

    def test_delete_vacancy(self):
        """
        Проверка удаления вакансии по индексу из файла.
        """
        self.json_saver.add_vacancy(self.vacancy)
        self.json_saver.add_vacancy(self.vacancy2)

        # Удаляем вакансию по индексу 0
        self.json_saver.delete_vacancy(0)

        vacancies = self.json_saver.get_vacancies()
        self.assertEqual(len(vacancies), 1)
        self.assertEqual(vacancies[0]['name'], 'Another Vacancy')

    def test_clear_vacancies(self):
        """
        Проверка полной очистки файла.
        """
        self.json_saver.add_vacancy(self.vacancy)
        self.json_saver.add_vacancy(self.vacancy2)

        self.json_saver.clear_vacancies()
        vacancies = self.json_saver.get_vacancies()
        self.assertEqual(len(vacancies), 0)


# ---
class TestUtils(unittest.TestCase):
    """
    Тестирование вспомогательных функций.
    """

    def setUp(self):
        """
        Подготовка к тестам.
        """
        self.vacancy1 = Vacancy({
            'name': 'Python Developer',
            'alternate_url': 'url1',
            'salary': {'from': 100000},
            'snippet': {'requirement': 'Опыт работы с Django.'}
        })
        self.vacancy2 = Vacancy({
            'name': 'Java Engineer',
            'alternate_url': 'url2',
            'salary': None,
            'snippet': {'requirement': 'Опыт работы с Spring.'}
        })
        self.vacancies_list = [self.vacancy1, self.vacancy2]

    def test_filter_vacancies_by_keywords(self):
        """
        Проверка фильтрации по ключевым словам.
        """
        # Поиск по ключевому слову в названии
        filtered = filter_vacancies_by_keywords(self.vacancies_list, ['python'])
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].name, 'Python Developer')

        # Поиск по ключевому слову в описании
        filtered = filter_vacancies_by_keywords(self.vacancies_list, ['django'])
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].name, 'Python Developer')

        # Поиск по двум ключевым словам
        filtered = filter_vacancies_by_keywords(self.vacancies_list, ['python', 'spring'])
        self.assertEqual(len(filtered), 2)
        self.assertIn(self.vacancy1, filtered)
        self.assertIn(self.vacancy2, filtered)

        # Поиск с пустым списком ключевых слов
        filtered = filter_vacancies_by_keywords(self.vacancies_list, [])
        self.assertEqual(len(filtered), 2)


if __name__ == '__main__':
    unittest.main()
