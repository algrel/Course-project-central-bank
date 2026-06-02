import pandas as pd

districts = {
    'центральный': 'Центральный',
    'дальневосточный': 'Дальневосточный',
    'приволжский': 'Приволжский',
    'северо-западный': 'Северо-Западный',
    'северо-кавказский': 'Северо-Кавказский',
    'сибирский': 'Сибирский',
    'уральский': 'Уральский',
    'южный': 'Южный'
}

def name(name):
    name = name.strip()
    name = name.lower()
    for a, b in districts.items():
        name = name.replace(a, b)
    name = name.replace('федеральный', 'федеральный')
    name = name.replace('округ', 'округ')
    return name


def get_geopoligon(name):
    if name in geo1:
        return geo1[name]
    for key in geo1.keys():
        if key.lower() == name.lower():
            return geo1[key]
    return ''  


df = pd.read_csv('federal_districts_before.csv', sep=';', encoding='utf-8')
df = df.rename(columns={df.columns[0]: 'Месяц'})
df['Месяц'] = pd.to_datetime(df['Месяц'])

geo = pd.read_csv('geopoligons.csv', sep=';', encoding='utf-8')
geo.columns = geo.columns.str.strip().str.replace('"', '')
geo['ФО'] = geo['ФО'].str.strip().str.replace('"', '')
geo1 = dict(zip(geo['ФО'], geo['ФО геополигон']))

rows = []

for i, row in df.iterrows():
    date = row['Месяц']
    for col in df.columns:
        if col == 'Месяц':
            continue
        if col.startswith('МСП'):
            type0 = 'МСП'
        elif col.startswith('Нефин'):
            type0 = 'Нефин'
        elif col.startswith('ФЛ'):
            type0 = 'ФЛ'
        else:
            continue
        
        if 'до 1 года' in col:
            term = 'До 1 года'
        elif 'свыше 1 года' in col:
            term = 'Свыше 1 года'
        else:
            continue
        
        district = col.replace('МСП ', '').replace('Нефин ', '').replace('ФЛ ', '')
        district = district.replace(' до 1 года', '').replace(' свыше 1 года', '')
        federal_district = name(district)
        geopoligon = get_geopoligon(federal_district)
        rows.append({'Месяц': date, 'ФО': federal_district, 'Геополигон': geopoligon, 'Категория': type0, 'Срок': term, 'Значение': row[col]})

result = pd.DataFrame(rows)
result = result.sort_values(['Месяц', 'ФО', 'Категория', 'Срок']).reset_index(drop=True)
result.to_csv('federal_districts_after.csv', index=False, encoding='utf-8-sig')
