from re import sub, compile
from csv import reader as read_csv


def csv_reader(file_name: str):
    with open(file_name, 'r', encoding='utf-8-sig') as file:
        lines = list(read_csv(file))

        titles = lines[0]
        rows = [line for line in lines[1:] if '' not in line and len(line) == len(titles)]
        return rows, titles


def text_cleaner(value):
    result = sub(compile('<.*?>'), '', value)
    if '\n' in result:
        return [' '.join(i.split()) for i in result.split('\n')]
    return ' '.join(result.split())


def csv_filter(reader, list_name):
    result = []
    for line in range(len(reader)):
        for elem in range(len(reader[line])):
            reader[line][elem] = text_cleaner(reader[line][elem])
        result.append(dict(zip(list_name, reader[line])))
    return result


def change(text):
    if isinstance(text, list):
        return ', '.join(text)
    if translate.keys().__contains__(text):
        return translate[text]
    return text


def print_vacancies(data_vacancies, dic_naming):
    for i in data_vacancies:
        translated = formatter(i)
        for j in translated:
            print(f'{j}: {translated[j]}')
        print()


def formatter(row: dict):
    formatted = {}
    s_from = format(int(float((row['salary_from']))), ',d').replace(',', ' ')
    s_to = format(int(float((row['salary_to']))), ',d').replace(',', ' ')
    s_gross = tax_dict[row["salary_gross"]]
    s_currency = translate[row["salary_currency"]]
    salary = f"{s_from} - {s_to} ({s_currency}) ({s_gross})"
    date = str(row["published_at"][0:10]).split('-')
    date = f"{date[2]}.{date[1]}.{date[0]}"
    row["salary_from"] = salary
    row["published_at"] = date
    decline_fields = ["salary_to", "salary_gross", "salary_currency"]
    for i in row:
        val = row.get(i)
        if not decline_fields.__contains__(i):
            if translate.__contains__(str(val)):
                formatted.update({translate[i]: ' '.join(translate[str(val)].split())})
            elif isinstance(val, list):
                formatted.update({translate[i]: ', '.join(val)})
            else:
                formatted.update({translate[i]: ' '.join(str(val).split())})
    return formatted


tax_dict = {'False': 'С вычетом налогов', 'True': 'Без вычета налогов', 'FALSE': 'С вычетом налогов',
            'TRUE': 'Без вычета налогов'}

translate = {'name': 'Название', 'description': 'Описание', 'key_skills': 'Навыки', 'experience_id': 'Опыт работы',
             'premium': 'Премиум-вакансия', 'employer_name': 'Компания', 'salary_from': 'Оклад',
             'salary_to': 'Верхняя граница вилки оклада', 'salary_gross': 'Оклад указан до вычета налогов',
             'salary_currency': 'Идентификатор валюты оклада', 'area_name': 'Название региона',
             'published_at': 'Дата публикации вакансии', 'noExperience': 'Нет опыта',
             'between1And3': 'От 1 года до 3 лет', 'between3And6': 'От 3 до 6 лет ', 'moreThan6': 'Более 6 лет',
             'AZN': 'Манаты', 'BYR': 'Белорусские рубли', 'EUR': 'Евро', 'GEL': 'Грузинский лари',
             'KGS': 'Киргизский сом', 'KZT': 'Тенге',
             'RUR': 'Рубли', 'UAH': 'Гривны', 'USD': 'Доллары', 'UZS': 'Узбекский сум', 'True': 'Да', 'False': 'Нет'}

file_nam = 'vacancies_medium.csv'
rows1, titles1 = csv_reader(file_nam)
print_vacancies(csv_filter(rows1, titles1), translate)
