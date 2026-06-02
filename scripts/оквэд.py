import pandas as pd
import re

df = pd.read_excel('оквэд_до.xlsx', sheet_name='Chart data')
df['Месяц'] = pd.to_datetime(df['Месяц'])

result_df = pd.melt(
    df, 
    id_vars=['Месяц'], 
    var_name='Категория', 
    value_name='Ставка'
)

def extract_borrower_type(category):
    if category.startswith('МСП'):
        return 'МСП'
    elif category.startswith('Нефин'):
        return 'Нефин'
    else:
        return None

def extract_loan_term(category):
    if 'до 1 года' in category:
        return 'До 1 года'
    elif 'свыше 1 года' in category:
        return 'Свыше 1 года'
    else:
        return None

def extract_okved(category):
    without_prefix = re.sub(r'^(МСП|Нефин)\s+', '', category)
    without_term = re.sub(r'\s+(до|свыше)\s+1\s+года$', '', without_prefix)
    without_letter = re.sub(r'^[A-ZА-Я]\.\s*', '', without_term)
    return without_letter.strip()

result_df['Тип_заемщика'] = result_df['Категория'].apply(extract_borrower_type)
result_df['Срок_кредита'] = result_df['Категория'].apply(extract_loan_term)
result_df['ОКВЭД'] = result_df['Категория'].apply(extract_okved)
result_df = result_df.drop('Категория', axis=1)
result_df = result_df[['Месяц', 'Тип_заемщика', 'ОКВЭД', 'Срок_кредита', 'Ставка']]
result_df = result_df.sort_values(['Месяц', 'Тип_заемщика', 'ОКВЭД', 'Срок_кредита']).reset_index(drop=True)
result_df.to_excel('оквэд_после.xlsx', index=False)

