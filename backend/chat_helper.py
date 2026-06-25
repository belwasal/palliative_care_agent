import os
import streamlit as st
import sqlite3
import pandas as pd


def get_hospices_data():
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(backend_dir)

    # Ищем базу данных в корне проекта
    db_path = os.path.join(root_dir, "hospices.db")

    if not os.path.exists(db_path):
        st.warning("База данных не найдена. Убедитесь, что вы запустили init_db.py")
        return pd.DataFrame()  # Возвращаем пустую таблицу, если базы нет

    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT name, address, phone FROM moscow_hospices", conn)
    conn.close()

    df = df.rename(columns={"name": "Название", "address": "Адрес", "phone": "Телефон"})

    return df


def get_instruction_text(file_name):
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(backend_dir)
    db_path = os.path.join(root_dir, "hospices.db")
    data_dir = os.path.join(root_dir, "data")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Создаем таблицу для инструкций, если её еще нет
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS instructions (
            name TEXT PRIMARY KEY,
            content TEXT NOT NULL
        )
    """)

    # Проверяем, пустая ли таблица. Загружаем в нее тексты из txt файлов
    cursor.execute("SELECT COUNT(*) FROM instructions")
    if cursor.fetchone()[0] == 0:
        files_to_load = ["doc_instruction.txt", "medicines.txt", "equipment.txt"]
        for txt_file in files_to_load:
            file_path = os.path.join(data_dir, txt_file)
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    # Записываем в базу: имя файла и сам текст
                    cursor.execute(
                        "INSERT INTO instructions (name, content) VALUES (?, ?)",
                        (txt_file, content),
                    )
        conn.commit()

    # Достаем нужную инструкцию из базы
    cursor.execute("SELECT content FROM instructions WHERE name = ?", (file_name,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]
    else:
        return None
