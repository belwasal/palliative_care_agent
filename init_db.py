import sqlite3
import os

# Путь, где будет создан файл базы данных
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hospices.db")


def create_and_populate_db():
    # Подключаемся к базе (файл создастся автоматически, если его нет)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Создаем таблицу с указанными полями
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS moscow_hospices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    """)

    # Очищаем таблицу перед добавлением, чтобы избежать дубликатов при перезапусках
    cursor.execute("DELETE FROM moscow_hospices")

    # Реальные данные по Москве: фонды, центры и хосписы
    data = [
        (
            'Фонд помощи хосписам "Вера"',
            "г. Москва, 2-й Николощеповский пер., 4",
            "8-800-700-84-36",
        ),
        (
            "Первый Московский хоспис им. В.В. Миллионщиковой",
            "г. Москва, ул. Доватора, 10",
            "+7 (499) 245-00-03",
        ),
        (
            "Центр паллиативной помощи ДЗМ",
            "г. Москва, ул. Двинцев, 6, стр. 2",
            "+7 (499) 940-19-50",
        ),
        (
            'Детский хоспис "Дом с маяком"',
            "г. Москва, ул. Долгоруковская, 30",
            "+7 (495) 120-00-50",
        ),
        ("Хоспис №2 (Дегунино)", "г. Москва, ул. Талдомская, 2А", "+7 (499) 488-44-64"),
        ("Хоспис №3 (Бутово)", "г. Москва, ул. Поляны, 4", "+7 (495) 714-35-08"),
    ]

    # Массово вставляем данные в таблицу
    cursor.executemany(
        """
        INSERT INTO moscow_hospices (name, address, phone)
        VALUES (?, ?, ?)
    """,
        data,
    )

    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()

    print(f"✅ База данных успешно создана: {db_path}")
    print(f"Добавлено записей: {len(data)}")


if __name__ == "__main__":
    create_and_populate_db()
