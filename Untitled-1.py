# %%
import pandas as pd
import streamlit as st
from collections import Counter

# %% [markdown]
# # Обзор данных

# %%
# uploaded_file = st.file_uploader("Выбирете файл", 
# help="Здесь может быть подсказка'")


# if uploaded_file is not None:
#      df = pd.read_csv(uploaded_file, sep='|')
#      df.columns = [
#         'task_id',
#         'task_name',
#         'status',
#         'communication_method',
#         'date_creation',
#         'customer_phone',
#         'plathorm']

#      # изменение типов
#      df['customer_phone'] = df['customer_phone'].astype(str)
#      df['task_id'] = df['task_id'].astype(int)
#      df['date_creation'] = pd.to_datetime(df['date_creation'], format='%Y-%m-%dT%H:%M:%S')

#      # удвление тестовых номеров, которые начинаются на 520...
#      df['phone'] = df.customer_phone.str[:3]
#      df = df[~df.phone.str.contains('520')]

#      # удаление пропусков, которые появляются из за особенностей выгрузки
#      df = df.dropna()
#      file_container = st.expander("Check your uploaded .csv")   
#      st.write(df)
# else:
#     st.info(
#         f"""
#              👆 Загрузите файл с расширением .csv
             
#              В файле должны стого содержаться следующие столбцы: id пользователя, id задачи, платформа, роль пользователя
#              """
#     )
#     st.stop()

# %%
st.write("""
**Поля датафрейма:**
- task_id - уникальный идентификатор задачи;
- task_name - название задачи;
- status - текущий статс задачи;
- communication_method - выбранный способ связи в приложении;
- date_creation - дата создания задачи в формате ГГГГ-ММ-ДД
- customer_phone - будет выступать в роли id пользователя""")

# %%
df = pd.read_csv('/Users/arturfattahov/Downloads/task_september_february.csv', sep='|')

df.columns = [
        'task_id',
        'task_name',
        'status',
        'communication_method',
        'date_creation',
        'customer_phone',
        'plathorm'
]

# изменение типов
df['customer_phone'] = df['customer_phone'].astype(str)
df['task_id'] = df['task_id'].astype(int)
df['date_creation'] = pd.to_datetime(df['date_creation'], format='%Y-%m-%dT%H:%M:%S')

# удвление тестовых номеров, которые начинаются на 520...
df['phone'] = df.customer_phone.str[:3]
df = df[~df.phone.str.contains('520')]

# удаление пропусков, которые появляются из за особенностей выгрузки
df = df.dropna()

df.info()
df.sample(2)

# %%
df = df.sort_values(by=['customer_phone', 'date_creation'])

# %%
df['diff'] = df.groupby('customer_phone')['date_creation'].diff()

# %% [markdown]
# # Фильтры по платформам

# %%
df["days"] = df["date_creation"].astype(str).str[0:10]

# %%
df = df[(df['days'] < '2022-01-28')]

# %%
df_admins = df[df['plathorm'] == 'admins']
df_ios = df[df['plathorm'] == 'ios']
df_andoid = df[df['plathorm'] == 'android']

# %% [markdown]
# # Рассчеты

# %%
st.write("""
# Рассчеты
""")

# %%
st.write("""
# Admins
""")

# %%
unique_users_admins = df_admins['customer_phone'].nunique()
number_tasks_admins = df_admins['task_id'].nunique()

st.write("Количество пользователей, которые создали хотя бы одну задачу:", unique_users_admins)
st.write("Количество созданных задач:", number_tasks_admins)

# %%



