import psycopg2


# Создаем класс для работы с БД
class DBManager:
    def __init__(self, params):
        self.conn = psycopg2.connect(**params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        query = ("SELECT company_name, count(*) from Kursovaya5.vacancies "
                 "group by company_name")
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
         названия вакансии и зарплаты и ссылки на вакансию"""
        query = "select company_name, vacancy_name, salary_from, salary_to, vacancy_url from Kursovaya5.vacancies"
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        query = "select avg((salary_from + salary_to) / 2) from Kursovaya5.vacancies"
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        query = ("select vacancy_name from Kursovaya5.vacancies where ((salary_from + salary_to) / 2)"
                 " > (select avg((salary_from + salary_to) / 2) from Kursovaya5.vacancies)")
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python"""
        query = f"select vacancy_name from Kursovaya5.vacancies where vacancy_name like '{keyword}'"
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows
