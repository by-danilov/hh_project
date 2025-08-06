from src.api_classes import HeadHunterAPI
from src.vacancy_class import Vacancy
from src.file_classes import JSONSaver
from src.utils import filter_vacancies_by_keywords, filter_vacancies_by_salary


def user_interaction():
    """
    Функция для взаимодействия с пользователем через консоль.
    """
    hh_api = HeadHunterAPI()
    json_saver = JSONSaver()

    print("Привет! Эта программа поможет тебе найти вакансии на hh.ru.")

    while True:
        print("\nВыберите действие:")
        print("1. Найти вакансии по поисковому запросу и сохранить их.")
        print("2. Показать все сохраненные вакансии.")
        print("3. Получить вакансии с ключевым словом в описании.")
        print("4. Отфильтровать вакансии по зарплате.")
        print("5. Получить топ N вакансий по зарплате.")
        print("6. Удалить вакансию из файла.")
        print("7. Полностью очистить файл от вакансий.")
        print("8. Выход.")

        choice = input("Введите номер действия: ")

        if choice == '1':
            search_query = input("Введите поисковый запрос (например, 'Python'): ")
            print(f"Ищу вакансии по запросу '{search_query}'...")
            hh_vacancies_data = hh_api.get_vacancies(search_query)

            if not hh_vacancies_data:
                print("Вакансии не найдены. Попробуйте другой запрос.")
                continue

            vacancies_list = [Vacancy(data) for data in hh_vacancies_data]
            print(f"Найдено {len(vacancies_list)} вакансий. Сохраняю в файл...")
            for vacancy in vacancies_list:
                json_saver.add_vacancy(vacancy)
            print("Вакансии успешно сохранены.")

        elif choice == '2':
            vacancies = json_saver.get_vacancies()
            if not vacancies:
                print("В файле нет сохраненных вакансий.")
            else:
                for v in vacancies:
                    vacancy_obj = Vacancy(v)
                    print(vacancy_obj)

        elif choice == '3':
            vacancies = json_saver.get_vacancies()
            if not vacancies:
                print("В файле нет сохраненных вакансий для фильтрации.")
                continue

            keywords_input = input("Введите ключевые слова для фильтрации через пробел: ")
            keywords = keywords_input.lower().split()

            vacancies_objs = [Vacancy(data) for data in vacancies]
            filtered_vacancies = filter_vacancies_by_keywords(vacancies_objs, keywords)

            if not filtered_vacancies:
                print("Вакансии по вашему запросу не найдены.")
            else:
                print(f"Найдено {len(filtered_vacancies)} вакансий, соответствующих вашим ключевым словам:")
                for v in filtered_vacancies:
                    print(v)

        elif choice == '4':
            vacancies = json_saver.get_vacancies()
            if not vacancies:
                print("В файле нет сохраненных вакансий для фильтрации.")
                continue

            try:
                min_salary = int(input("Введите минимальную зарплату: "))
                max_salary = int(input("Введите максимальную зарплату: "))

                vacancies_objs = [Vacancy(data) for data in vacancies]
                filtered_vacancies = filter_vacancies_by_salary(vacancies_objs, min_salary, max_salary)

                if not filtered_vacancies:
                    print("Вакансии в заданном диапазоне зарплат не найдены.")
                else:
                    print(f"Найдено {len(filtered_vacancies)} вакансий в диапазоне от {min_salary} до {max_salary}:")
                    for v in filtered_vacancies:
                        print(v)
            except ValueError:
                print("Некорректный ввод. Пожалуйста, введите числа.")

        elif choice == '5':
            try:
                top_n = int(input("Введите количество вакансий для вывода в топ N: "))
                vacancies = json_saver.get_vacancies()
                if not vacancies:
                    print("В файле нет сохраненных вакансий для сортировки.")
                    continue

                vacancies_objs = [Vacancy(data) for data in vacancies]
                sorted_vacancies = sorted(vacancies_objs, reverse=True)

                print(f"\nТоп {top_n} вакансий по зарплате:")
                for i in range(min(top_n, len(sorted_vacancies))):
                    print(sorted_vacancies[i])

            except ValueError:
                print("Некорректный ввод. Пожалуйста, введите число.")
                continue

        elif choice == '6':
            vacancies = json_saver.get_vacancies()
            if not vacancies:
                print("В файле нет сохраненных вакансий для удаления.")
                continue

            print("Список сохраненных вакансий:")
            for i, v in enumerate(vacancies):
                print(f"{i + 1}. {v['name']}")

            try:
                index_to_delete = int(input("Введите номер вакансии для удаления: ")) - 1

                if 0 <= index_to_delete < len(vacancies):
                    json_saver.delete_vacancy(index_to_delete)
                else:
                    print("Некорректный номер.")
            except ValueError:
                print("Некорректный ввод. Пожалуйста, введите число.")

        elif choice == '7':
            json_saver.clear_vacancies()

        elif choice == '8':
            print("Спасибо за использование программы. До свидания!")
            break

        else:
            print("Некорректный выбор. Пожалуйста, введите число от 1 до 8.")


if __name__ == "__main__":
    user_interaction()
