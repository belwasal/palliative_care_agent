import streamlit as st
import os
import sys
import sqlite3
import pandas as pd
import requests

# Путь к корню проекта
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)

# Добавление корня в системный путь (для backend)
sys.path.append(root_dir)

from backend.chat_helper import get_hospices_data

st.set_page_config(page_title="С любовью можно прожить", page_icon="💙", layout="wide")

title, draw = st.columns([4, 1])

with title:
    # Title
    current_dir = os.path.dirname(os.path.abspath(__file__))
    title_path = os.path.join(current_dir, "handwritten_title_clear.png")
    st.image(title_path, use_container_width=True, output_format="PNG")

    st.markdown(
        """
        <p style="font-size: 14px; font-style: italic; color: #888888; margin-top: -10px; margin-bottom: 25px;">
            Искренняя поддержка для тех, кто заботится о близких в трудную минуту
        </p>
        """,
        unsafe_allow_html=True,
    )

    # Приветствие
    st.write(
        "Здравствуйте. Вы не одни. Я здесь, чтобы бережно провести вас через все формальности. Моя задача — сделать так, чтобы вы тратили время на близких, а поиск нужной информации я возьму на себя."
    )
    st.write(
        "Подскажите, что вам сейчас нужно? Выберите раздел ниже или задайте любой вопрос."
    )


st.divider()


def toggle_api_instruction(button_key, file_name, button_text, icon):
    # Задаем начальное состояние
    if button_key not in st.session_state:
        st.session_state[button_key] = False

    # Переход по кнопке
    if st.button(button_text, icon=icon, use_container_width=True):
        st.session_state[button_key] = not st.session_state[button_key]

    # Если кнопка вкл, делаем запрос к API
    if st.session_state[button_key]:
        try:
            response = requests.get(f"http://backend:8080/api/instructions/{file_name}")
            if response.status_code == 200:
                data = response.json()
                st.markdown(data["content"])
            else:
                st.error("Файл с инструкцией не найден в базе.")
        except requests.exceptions.ConnectionError:
            st.error("Не удалось подключиться к серверу.")


# Buttons
first_col, second_col = st.columns(2)

with first_col:
    # Кнопка для документов
    toggle_api_instruction(
        "btn_docs",
        "doc_instruction.txt",
        "Сбор документов на учет",
        ":material/description:",
    )

    # Кнопка для лекарств
    toggle_api_instruction(
        "btn_meds", "medicines.txt", "Получение лекарств", ":material/medication:"
    )

with second_col:
    # Кнопка для оборудования
    toggle_api_instruction(
        "btn_equip", "equipment.txt", "Запрос оборудования", ":material/accessible:"
    )

    # Адреса фондов и хосписов
    if "show_hospices" not in st.session_state:
        st.session_state.show_hospices = False

    if st.button(
        "Адреса фондов и хосписов",
        icon=":material/location_on:",
        use_container_width=True,
    ):
        st.session_state.show_hospices = not st.session_state.show_hospices

    if st.session_state.show_hospices:
        response = requests.get("http://backend:8080/api/hospices")
        data = response.json()

        df = pd.DataFrame(data)
        st.markdown("**Адреса проверенных фондов и хосписов в Москве:**")

        df["Телефон"] = (
            df["Телефон"].str.replace(" ", "\xa0").str.replace("-", "\u2011")
        )

        html_table = df.to_html(index=False, escape=False)

        st.markdown(html_table, unsafe_allow_html=True)
