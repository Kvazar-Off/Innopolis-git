import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import ttest_ind, mannwhitneyu, chi2_contingency
import time


def up_file():
    st.title("Загрузка и обработка CSV файла")

    uploaded_file = st.file_uploader("Выберите CSV файл", type=["csv"])

    data_frame = None

    if uploaded_file is not None:
        try:
            data_frame = pd.read_csv(uploaded_file)
            success_message = st.success("Файл успешно загружен.")
            time.sleep(1)
            success_message.empty()

            st.write("Первые несколько строк файла:")
            st.dataframe(data_frame.head())

        except Exception as e:
            st.error(f"Ошибка при загрузке файла: {e}")
            st.warning('Загрузите файл заново.')
    return data_frame

def plot_distribution_chart(data_frame, column_name):
    is_categorical = data_frame[column_name].dtype == 'object'

    if is_categorical:
        st.title(f"Распределение категориальных данных по {column_name}")
        fig = px.pie(data_frame, names=column_name, title=f"Круговая диаграмма распределение категориальных данных по {column_name}")
    else:
        st.title(f"Распределения числовых данных по {column_name}")
        fig = px.histogram(data_frame, x=column_name, title=f"Гистограмма распределения числовых данных по {column_name}")

    st.plotly_chart(fig)

def t_test(data_frame, col1, col2):
    st.title("t-тест")

    group1 = data_frame[col1]
    group2 = data_frame[col2]

    t_stat, p_value = ttest_ind(group1, group2)

    st.write(f"t-статистика: {t_stat:.4f}")
    st.write(f"P-значение: {p_value:.4f}")

    if p_value < 0.05:
        st.write(f"Различия между {col1} и {col2}статистически значимы.")
    else:
        st.write(f"Различия между {col1} и {col2} статистически незначимы.")

def mann_whitney_u_test(data_frame, col1, col2):
    st.title("U-тест Манна-Уитни")

    group1 = data_frame[col1]
    group2 = data_frame[col2]

    u_stat, p_value = mannwhitneyu(group1, group2)

    st.write(f"U-статистика: {u_stat:.4f}")
    st.write(f"P-значение: {p_value:.4f}")

    if p_value < 0.05:
        st.write(f"Различия между {col1} и {col2} статистически значимы.")
    else:
        st.write(f"Различия между {col1} и {col2} статистически незначимы.")

def chi_square_test(data_frame, col1, col2):
    st.title("Тест хи-квадрат")

    contingency_table = pd.crosstab(data_frame[col1], data_frame[col2])

    chi2, p, dof, expected = chi2_contingency(contingency_table)

    st.write(f"Статистика хи-квадрат: {chi2:.4f}")
    st.write(f"P-значение: {p:.4f}")
    st.write(f"Степени свободы: {dof:.4f}")
    st.write("Ожидаемые частоты:")
    st.write(expected)

    if p < 0.05:
        st.write("Существуют статистически значимые зависимости между переменными.")
    else:
        st.write("Зависимостей между переменными не обнаружено.")

def main():
    #st.balloons()
    st.markdown('Домашнее задание по темам :blue["Статистика"], :red["Визуализация"], :green["Развертывание в виде веб приложения"]')
    st.markdown("**ФИО:** _Трифонов Сергей Алексеевич_")

    data_frame = up_file()

    if data_frame is not None and not data_frame.empty:
        first_column = st.selectbox("Выберите колонку для исследования", data_frame.columns)
        second_column = st.selectbox("Выберите колонку для исследования", data_frame.columns, key=2)

        if first_column != second_column:
            plot_distribution_chart(data_frame, first_column)
            plot_distribution_chart(data_frame, second_column)
        else:
            st.warning("Выберите разные колонки для корректного анализа.")
            return



        if data_frame[first_column].dtype == 'object' or data_frame[second_column].dtype == 'object':
            try:
                chi_square_test(data_frame, first_column, second_column)
            except ValueError as chi2_exception:
                st.error(f"Ошибка при проведении теста хи-квадрат: {chi2_exception}")
        else:
            tests = st.selectbox("Выберите метод проверки гипотез:", ('t-test', 'u-test'))
            try:
                if tests == 't-test':
                    t_test(data_frame, first_column, second_column)
                else:
                    mann_whitney_u_test(data_frame, first_column, second_column)
            except Exception as test_exception:
                st.error(f"Ошибка при проведении статистического теста: {test_exception}")

if __name__ == "__main__":
    main()
