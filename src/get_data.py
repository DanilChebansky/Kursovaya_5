import requests


# Создаем словарь с названием компании и её id на сайте hh.ru
companies_data = {
        'Тиньков': 78638,
        'Яндекс': 1740,
        'МегаФон': 3127,
        'Сбербанк': 1473866,
        'Банк ВТБ': 4181,
        'Газпромнефть': 39305,
        'Альфа-банк': 80,
        'ИНЖИНИРИНГОВЫЙ ДИВИЗИОН ГОСКОРПОРАЦИИ РОСАТОМ': 107434,
        'Гринатом': 665467,
        'Госкорпорация Росатом': 577743
    }


def load_vacancies(list_):
    """Ищет вакансии на 8 страницах списка вакансий каждого работодателя и возвращает заполненный список
     с характеристиками этих вакансий"""
    vacans = []
    for company in companies_data.values():
        url = f'https://api.hh.ru/vacancies?employer_id={company}'
        headers = {'User-Agent': 'HH-User-Agent'}
        params = {'page': 0, 'per_page': 100, "currency": "RUR", "only_with_salary": True}
        while params.get('page') != 8:
            response = requests.get(url, headers=headers, params=params)
            vacanci = response.json()['items']
            vacans.extend(vacanci)
            params['page'] += 1
    for vacancy in vacans:
        vacancy_id = vacancy['id']
        vacancy_name = vacancy['name']
        company_id = vacancy['employer']['id']
        company_name = vacancy['employer']['name']
        vacancy_url = vacancy['alternate_url']
        if vacancy['snippet']['responsibility'] is None:
            description = "Нет описания"
        else:
            description = vacancy['snippet']['responsibility']
        if vacancy['snippet']['requirement'] is None:
            requirements = "Нет требований"
        else:
            requirements = vacancy['snippet']['requirement']
        if vacancy['salary']['from'] is None:
            salary_from = 0
        else:
            salary_from = vacancy['salary']['from']
        if vacancy['salary']['to'] is None:
            salary_to = int(int(salary_from) * 1.5)
        else:
            salary_to = vacancy['salary']['to']
        vacanc = {
            "vacancy_id": vacancy_id,
            "vacancy_name": vacancy_name,
            "company_id": company_id,
            "company_name": company_name,
            "vacancy_url": vacancy_url,
            "description": description,
            "requirements": requirements,
            "salary_from": salary_from,
            "salary_to": salary_to
        }
        list_.append(vacanc)
    return list_


def load_companies(list_):
    """Заполняет список характеристик работодателей (id, название и ссылка на страницу на hh.ru"""
    for company_name, company_id in companies_data.items():
        company_url = f'https://hh.ru/employer/{company_id}'
        company = {"company_id": company_id, "company_name": company_name, "company_url": company_url}
        list_.append(company)
    return list_
