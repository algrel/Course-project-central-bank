import pandas as pd
import re

def type(s):
    if s.startswith('МСП'):
        return 'МСП'
    elif s.startswith('Нефин'):
        return 'Нефин'

def term(s):
    if 'до 1 года' in s:
        return 'До 1 года'
    elif 'свыше 1 года' in s:
        return 'Свыше 1 года'

def okved(s):
    res = re.sub(r'^(МСП|Нефин)\s+', '', s)
    res = re.sub(r'\s+(до|свыше)\s+1\s+года$', '', s)
    res = re.sub(r'^[A-ZА-Я]\.\s*', '', s)
    return res.strip()


df = pd.read_excel('okved_before.xlsx', sheet_name='Chart data')
df['Месяц'] = pd.to_datetime(df['Месяц'])
result = pd.melt(df, id_vars=['Месяц'], var_name='Категория', value_name='Ставка')
result['Тип_заемщика'] = result['Категория'].apply(type)
result['Срок_кредита'] = result['Категория'].apply(term)
result['ОКВЭД'] = result['Категория'].apply(okved)
result = result.drop('Категория', axis=1)
result = result[['Месяц', 'Тип_заемщика', 'ОКВЭД', 'Срок_кредита', 'Ставка']].sort_values(['Месяц', 'Тип_заемщика', 'ОКВЭД', 'Срок_кредита']).reset_index(drop=True)
result.to_excel('okved_after.xlsx', index=False)
