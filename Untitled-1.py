# %%
import pandas as pd
import streamlit as st
from collections import Counter

# %% [markdown]
# # Обзор данных

# %%
st.set_page_config(page_title="Количество задач")


uploaded_file = st.file_uploader("Выбирете файл")


if uploaded_file is not None:
     df = pd.read_csv(uploaded_file, sep='|')
     df.columns = [
        'task_id',
        'task_name',
        'status',
        'communication_method',
        'date_creation',
        'customer_phone',
        'plathorm']

     # изменение типов
     df['customer_phone'] = df['customer_phone'].astype(str)
     df['task_id'] = df['task_id'].astype(int)
     df['date_creation'] = pd.to_datetime(df['date_creation'], format='%Y-%m-%dT%H:%M:%S')

     # удвление тестовых номеров, которые начинаются на 520...
     df['phone'] = df.customer_phone.str[:3]
     df = df[~df.phone.str.contains('520')]

     # удаление пропусков, которые появляются из за особенностей выгрузки
     df = df.dropna()
     file_container = st.expander("Check your uploaded .csv")   
     st.write(df)
else:
    st.info(
        f"""
             👆 Загрузите файл с расширением .csv
             В файле должны стого содержаться следующие столбцы:
             - id задачи, название задачи
             - текущий статус задачи
             - выбранный способ связи в приложении
             - дата создания задачи в формате ГГГГ-ММ-ДД
             - телефон заказчика
             """
    )
    st.stop()

# %%
st.write("""
**Поля датафрейма:**
- task_id - уникальный идентификатор задачи;
- task_name - название задачи;
- status - текущий статус задачи;
- communication_method - выбранный способ связи в приложении;
- date_creation - дата создания задачи в формате ГГГГ-ММ-ДД
- customer_phone - телефон заказчика""")

# %%
# df = pd.read_csv('/Users/arturfattahov/Downloads/task_september_february.csv', sep='|')

# df.columns = [
#         'task_id',
#         'task_name',
#         'status',
#         'communication_method',
#         'date_creation',
#         'customer_phone',
#         'plathorm'
# ]

# # изменение типов
# df['customer_phone'] = df['customer_phone'].astype(str)
# df['task_id'] = df['task_id'].astype(int)
# df['date_creation'] = pd.to_datetime(df['date_creation'], format='%Y-%m-%dT%H:%M:%S')

# # удвление тестовых номеров, которые начинаются на 520...
# df['phone'] = df.customer_phone.str[:3]
# df = df[~df.phone.str.contains('520')]

# # удаление пропусков, которые появляются из за особенностей выгрузки
# df = df.dropna()

# df.info()
# df.sample(2)

# %%
df = df.sort_values(by=['customer_phone', 'date_creation'])

# %%
df['diff'] = df.groupby('customer_phone')['date_creation'].diff()

# %% [markdown]
# # Фильтры по платформам

# %%
# df["days"] = df["date_creation"].astype(str).str[0:10]

# %%
# df = df[(df['days'] < '2022-01-28')]

# %%
df_admins = df[df['plathorm'] == 'admins']
df_ios = df[df['plathorm'] == 'ios']
df_andoid = df[df['plathorm'] == 'android']

# %% [markdown]
# # Рассчеты

# %%
st.write("""# Рассчеты""")

# %%
st.write("""## Admins""")

# %%
unique_users_admins = df_admins['customer_phone'].nunique()
number_tasks_admins = df_admins['task_id'].nunique()

st.write("Количество пользователей, которые создали хотя бы одну задачу:", unique_users_admins)
st.write("Количество созданных задач:", number_tasks_admins)

# %%
st.write("""## iOS""")

# %%
unique_users_ios = df_ios['customer_phone'].nunique()
number_tasks_ios= df_ios['task_id'].nunique()

st.write("Количество пользователей, которые создали хотя бы одну задачу:", unique_users_ios)
st.write("Количество созданных задач:", number_tasks_ios)

# %%
st.write("""## Android""")

# %%
unique_users_android = df_andoid['customer_phone'].nunique()
number_tasks_android = df_andoid['task_id'].nunique()

st.write("Количество пользователей, которые создали хотя бы одну задачу:", unique_users_android)
st.write("Количество созданных задач:", number_tasks_android)

# %%
st.write("""### Распределение пользователей по платформе""")

# %%
platform_distribution = Counter(df['plathorm'])

st.write("Количество созданных задач:", platform_distribution)

# %% [markdown]
# # Повторные задачи

# %%
st.write("""# Повторные задачи""")

# %%
df = df.loc[df['diff'] > '120 seconds']
df_admins_new = df[df['plathorm'] == 'admins']
df_ios_new = df[df['plathorm'] == 'ios']
df_android_new = df[df['plathorm'] == 'android']

# %% [markdown]
# ## Admins

# %%
st.write("""## Admins""")

# %%
unique_users_new_df_admins = df_admins_new['customer_phone'].nunique()

st.write("Количество пользователей, которые создали хотя бы одну повторную  задачу:", unique_users_new_df_admins)
st.write('Процент повторных задач в панели администратора: {:.0f}%'
        .format(unique_users_new_df_admins * 100 / unique_users_admins))

# %% [markdown]
# ## iOS

# %%
st.write("""## iOS""")

# %%
unique_users_new_df_ios = df_ios_new['customer_phone'].nunique()

st.write("Количество пользователей, которые создали хотя бы одну повторную  задачу:", unique_users_new_df_ios)
st.write('Процент повторных задач iOS: {:.0f}%'
        .format(unique_users_new_df_ios * 100 / unique_users_ios))

# %% [markdown]
# ## Android

# %%
st.write("""## Android""")

# %%
unique_users_new_df_android = df_android_new['customer_phone'].nunique()

st.write("Количество пользователей, которые создали хотя бы одну повторную  задачу:", unique_users_new_df_android)
st.write('Процент повторных задач iOS: {:.0f}%'
        .format(unique_users_new_df_android * 100 / unique_users_android))

# %% [markdown]
# # Медиана и среднее значение

# %%
st.write("""# Медиана и среднее значение""")

# %% [markdown]
# ## Admins

# %%
st.write("""## Admins""")

# %%
st.write('Среднее повторной задачи Admins', df_admins_new['diff'].mean())
st.write('Медиана повторной задачи Admins', df_admins_new['diff'].median())

# %% [markdown]
# ## iOS

# %%
st.write("""## iOS""")

# %%
st.write('Среднее повторной задачи iOS', df_ios_new['diff'].mean())
st.write('Медиана повторной задачи iOS', df_ios_new['diff'].median())

# %% [markdown]
# ## Android

# %%
st.write("""## Android""")

# %%
st.write('Среднее повторной задачи Android', df_android_new['diff'].mean())
st.write('Медиана повторной задачи Android', df_android_new['diff'].median())

# %% [markdown]
# # Распределение по дням

# %%
st.write("""# Распределение по дням""")

# %%
def creation_day(day):
    if int(day.days) <= 2:
        return 'Меньше 2 дней'
    elif 3 <= int(day.days) < 5:
        return 'От 2 до 5 дней'
    elif 5 <= int(day.days) < 10:
        return 'От 5 до 10 дней'
    elif 10 <= int(day.days) < 20:
        return 'От 10 до 20 дней'
    elif 20 <= int(day.days) < 50:
        return 'От 20 до 50 дней'
    else:
        return 'Более 50 дней'

# %% [markdown]
# ## Admins

# %%
st.write("""# Admins""")

# %%
st.write('Распределение повторных задач Admins', df_admins_new['diff'].apply(creation_day).value_counts())

# %% [markdown]
# ## iOS

# %%
st.write("""# iOS""")

# %%
st.write('Распределение повторных задач iOS', df_ios_new['diff'].apply(creation_day).value_counts())

# %% [markdown]
# ## Android

# %%
st.write("""# Android""")

# %%
st.write('Распределение повторных задач Android', df_android_new['diff'].apply(creation_day).value_counts())

# %%



