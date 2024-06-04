from src.get_data import load_companies, load_vacancies
import psycopg2
from src.dbmanager import DBManager

# Создаем пустые списки для характеристик вакансий и работодателей
vacancies = []
employers = []

# Заполняем эти списки данными с сайта hh.ru
load_vacancies(vacancies)
load_companies(employers)

# Вписываем нужные параметры для входа в базу данных
params = {"host": "localhost", "database": "postgres", "user": "postgres", "password": "1111"}

# Соединяемся с базой данных
conn = psycopg2.connect(**params)
cur = conn.cursor()

# Создаем схему и удаляем таблицы для предотвращения ошибок перед их созданием
cur.execute("create schema if not exists Kursovaya5;")
cur.execute("DROP TABLE IF EXISTS Kursovaya5.vacancies")
cur.execute("DROP TABLE IF EXISTS Kursovaya5.employers")

# Создаем таблицы с нужными колонками
cur.execute("CREATE TABLE Kursovaya5.vacancies("
            "vacancy_id INT,"
            "vacancy_name VARCHAR(255) NOT NULL,"
            "company_id INT NOT NULL,"
            "company_name VARCHAR(255) NOT NULL,"
            "vacancy_url VARCHAR(255) NOT NULL,"
            "description TEXT NOT NULL,"
            "requirements TEXT NOT NULL,"
            "salary_from INT NOT NULL,"
            "salary_to INT NOT NULL)")

cur.execute("CREATE TABLE Kursovaya5.employers("
            "company_id INT,"
            "company_name VARCHAR(255) NOT NULL,"
            "company_url VARCHAR(255) NOT NULL)")

# Сохраняем изменения
conn.commit()

# Заполняем таблицы данными из списков и сохраняем изменения
for vacancy in vacancies:
    cur.execute("INSERT INTO Kursovaya5.vacancies (vacancy_id, vacancy_name, company_id, company_name, vacancy_url,"
                "description, requirements, salary_from, salary_to) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (vacancy['vacancy_id'], vacancy['vacancy_name'], vacancy['company_id'], vacancy['company_name'],
                 vacancy['vacancy_url'], vacancy['description'], vacancy['requirements'], vacancy['salary_from'],
                 vacancy['salary_to']))
conn.commit()

for employer in employers:
    cur.execute("INSERT INTO Kursovaya5.employers (company_id, company_name, company_url) VALUES (%s, %s, %s)",
                (employer['company_id'], employer['company_name'], employer['company_url']))
conn.commit()

dbmanager = DBManager(params)

# Начинаем цикл, где пользователь или выбирает нужное действие с БД и цикл прерывается, или после неверного ввода
# цикл начинается заново
while True:
    print(f"Какое действие желаете произвести? Нажмите соответстующую цифру:\n"
          f"1 - получить список всех компаний и количество вакансий у каждой компании\n"
          f"2 - получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и"
          f" ссылки на вакансию\n"
          f"3 - получить среднюю зарплату по вакансиям\n"
          f"4 - получить список всех вакансий, у которых зарплата выше средней по всем вакансиям\n"
          f"5 - получить список всех вакансий, в названии которых содержатся переданные в метод слова, например "
          f"python\n")

    user_input = int(input())
    if user_input == 1:
        rows = dbmanager.get_companies_and_vacancies_count()
        print(rows)
        break
    elif user_input == 2:
        rows = dbmanager.get_all_vacancies()
        print(rows)
        break
    elif user_input == 3:
        rows = dbmanager.get_avg_salary()
        print(rows)
        break
    elif user_input == 4:
        rows = dbmanager.get_vacancies_with_higher_salary()
        print(rows)
        break
    elif user_input == 5:
        keyword_input = input("Введите ключевое слово")
        rows = dbmanager.get_vacancies_with_keyword(keyword_input)
        print(rows)
        break
    else:
        print("Вы ввели что-то не то, повторите запрос")

cur.close()
conn.close()
