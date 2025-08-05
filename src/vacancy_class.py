class Vacancy:
    """
    Класс для представления и обработки данных о вакансии.
    """
    __slots__ = ('name', 'url', 'salary_from', 'salary_to', 'currency', 'description')

    def __init__(self, vacancy_data: dict):
        """
        Инициализация экземпляра класса Vacancy.
        :param vacancy_data: Словарь с данными о вакансии.
        """
        self.name = vacancy_data.get('name')

        # Проверяем, в каком формате пришла зарплата
        if 'salary' in vacancy_data:
            # Данные от API
            salary = vacancy_data.get('salary')
            self.__validate_salary(salary)
            self.url = vacancy_data.get('alternate_url') if vacancy_data.get('alternate_url') else 'Ссылка не указана'

            snippet = vacancy_data.get('snippet', {})
            self.description = snippet.get('requirement') if snippet.get('requirement') else 'Описание не указано.'
        else:
            # Данные из нашего JSON-файла
            self.salary_from = vacancy_data.get('salary_from', 0)
            self.salary_to = vacancy_data.get('salary_to', 0)
            self.currency = vacancy_data.get('currency', 'Зарплата не указана')
            self.url = vacancy_data.get('url') if vacancy_data.get('url') else 'Ссылка не указана'
            self.description = vacancy_data.get('description') if vacancy_data.get(
                'description') else 'Описание не указано.'

    def __validate_salary(self, salary: dict):
        """
        Приватный метод для валидации данных о зарплате.
        """
        if salary:
            self.salary_from = salary.get('from') if salary.get('from') is not None else 0
            self.salary_to = salary.get('to') if salary.get('to') is not None else 0
            self.currency = salary.get('currency') if salary.get('currency') else 'Зарплата не указана'
        else:
            self.salary_from = 0
            self.salary_to = 0
            self.currency = 'Зарплата не указана'

    def __lt__(self, other: 'Vacancy'):
        """
        Метод для сравнения вакансий по зарплате (меньше).
        """
        if self.salary_from and not other.salary_from:
            return False
        if not self.salary_from and other.salary_from:
            return True
        return self.salary_from < other.salary_from

    def __le__(self, other: 'Vacancy'):
        """
        Метод для сравнения вакансий по зарплате (меньше или равно).
        """
        if self.salary_from and not other.salary_from:
            return False
        if not self.salary_from and other.salary_from:
            return True
        return self.salary_from <= other.salary_from

    def __gt__(self, other: 'Vacancy'):
        """
        Метод для сравнения вакансий по зарплате (больше).
        """
        if self.salary_from and not other.salary_from:
            return True
        if not self.salary_from and other.salary_from:
            return False
        return self.salary_from > other.salary_from

    def __ge__(self, other: 'Vacancy'):
        """
        Метод для сравнения вакансий по зарплате (больше или равно).
        """
        if self.salary_from and not other.salary_from:
            return True
        if not self.salary_from and other.salary_from:
            return False
        return self.salary_from >= other.salary_from

    def __eq__(self, other: 'Vacancy'):
        """
        Метод для сравнения вакансий по зарплате (равно).
        """
        return self.salary_from == other.salary_from and self.salary_to == other.salary_to

    def __str__(self):
        """
        Строковое представление объекта Vacancy для удобного вывода.
        """
        if self.salary_from or self.salary_to:
            if self.salary_from and self.salary_to:
                salary_info = f'{self.salary_from} - {self.salary_to} {self.currency}'
            elif self.salary_from:
                salary_info = f'от {self.salary_from} {self.currency}'
            else:
                salary_info = f'до {self.salary_to} {self.currency}'
        else:
            salary_info = 'Зарплата не указана'

        return f"Вакансия: {self.name}\nЗарплата: {salary_info}\nСсылка: {self.url}\nТребования: {self.description}\n"
