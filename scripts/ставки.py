import pandas as pd

df = pd.read_excel('ставки_до.xlsx', sheet_name='Chart data')
df['Месяц'] = pd.to_datetime(df['Месяц'])
type_mapping = {
    'МСП до 1 года': 'МСП',
    'МСП свыше 1 года': 'МСП',
    'Нефин до 1 года': 'Нефин',
    'Нефин свыше 1 года': 'Нефин',
    'ФЛ до 1 года': 'ФЛ',
    'ФЛ свыше 1 года': 'ФЛ'
}

term_mapping = {
    'МСП до 1 года': 'До 1 года',
    'МСП свыше 1 года': 'Свыше 1 года',
    'Нефин до 1 года': 'До 1 года',
    'Нефин свыше 1 года': 'Свыше 1 года',
    'ФЛ до 1 года': 'До 1 года',
    'ФЛ свыше 1 года': 'Свыше 1 года'
}

result_df = pd.melt(
    df, 
    id_vars=['Месяц'], 
    var_name='Категория', 
    value_name='Ставка'
)

result_df['Тип_заемщика'] = result_df['Категория'].map(type_mapping)
result_df['Срок_кредита'] = result_df['Категория'].map(term_mapping)
result_df = result_df.sort_values(['Месяц', 'Категория']).reset_index(drop=True)
result_df.to_excel('ставки_после.xlsx', index=False)
