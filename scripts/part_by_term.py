import pandas as pd

types = {
    'МСП до 1 года': 'МСП',
    'МСП свыше 1 года': 'МСП',
    'Нефин до 1 года': 'Нефин',
    'Нефин свыше 1 года': 'Нефин',
    'ФЛ до 1 года': 'ФЛ',
    'ФЛ свыше 1 года': 'ФЛ'
}

terms = {
    'МСП до 1 года': 'До 1 года',
    'МСП свыше 1 года': 'Свыше 1 года',
    'Нефин до 1 года': 'До 1 года',
    'Нефин свыше 1 года': 'Свыше 1 года',
    'ФЛ до 1 года': 'До 1 года',
    'ФЛ свыше 1 года': 'Свыше 1 года'
}


df = pd.read_excel('part_by_term_before.xlsx', sheet_name='Chart data')
df['Месяц'] = pd.to_datetime(df['Месяц'])
result = pd.melt(df, id_vars=['Месяц'], var_name='Категория', value_name='Соотношение')
result['Тип_заемщика'] = result['Категория'].map(types)
result['Срок_кредита'] = result['Категория'].map(terms)
result = result.sort_values(['Месяц', 'Категория']).reset_index(drop=True)
result.to_excel('part_by_term_after.xlsx', index=False)
