import pandas as pd

df = pd.read_csv('фо_дата.csv', sep=';', encoding='utf-8')
geo_df = pd.read_csv('фо гео.csv', sep=';', encoding='utf-8')
geo_df.columns = geo_df.columns.str.strip().str.replace('"', '')
geo_df['ФО'] = geo_df['ФО'].str.strip().str.replace('"', '')
geo_dict = dict(zip(geo_df['ФО'], geo_df['ФО геополигон']))
df = df.rename(columns={df.columns[0]: 'Месяц'})
df['Месяц'] = pd.to_datetime(df['Месяц'])


def normalize_district_name(name):
    name = name.strip()
    name = name.lower()
    replacements = {
        'центральный': 'Центральный',
        'дальневосточный': 'Дальневосточный',
        'приволжский': 'Приволжский',
        'северо-западный': 'Северо-Западный',
        'северо-кавказский': 'Северо-Кавказский',
        'сибирский': 'Сибирский',
        'уральский': 'Уральский',
        'южный': 'Южный'
    }
    for old, new in replacements.items():
        name = name.replace(old, new)
    name = name.replace('федеральный', 'федеральный')
    name = name.replace('округ', 'округ')
    return name

def get_geo_polygon(district_name):
    if district_name in geo_dict:
        return geo_dict[district_name]
    for key in geo_dict.keys():
        if key.lower() == district_name.lower():
            return geo_dict[key]
    return ''  

rows = []

for _, row in df.iterrows():
    date = row['Месяц']
    for col in df.columns:
        if col == 'Месяц':
            continue
        
        if col.startswith('МСП'):
            category = 'МСП'
        elif col.startswith('Нефин'):
            category = 'Нефин'
        elif col.startswith('ФЛ'):
            category = 'ФЛ'
        else:
            continue
        
        if 'до 1 года' in col:
            term = 'До 1 года'
        elif 'свыше 1 года' in col:
            term = 'Свыше 1 года'
        else:
            continue
        
        district_raw = col.replace('МСП ', '').replace('Нефин ', '').replace('ФЛ ', '')
        district_raw = district_raw.replace(' до 1 года', '').replace(' свыше 1 года', '')
        district = normalize_district_name(district_raw)
        geo_polygon = get_geo_polygon(district)
        
        rows.append({
            'Месяц': date,
            'ФО': district,
            'Геополигон': geo_polygon,
            'Категория': category,
            'Срок': term,
            'Значение': row[col]
        })

result_df = pd.DataFrame(rows)
result_df = result_df.sort_values(['Месяц', 'ФО', 'Категория', 'Срок']).reset_index(drop=True)
result_df.to_csv('фо_после.csv', index=False, encoding='utf-8-sig')
