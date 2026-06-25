from fastapi import FastAPI
import os
import sys
import pandas as pd

# Добавляем корень проекта в пути, чтобы импорты не ломались
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

from backend.chat_helper import get_hospices_data, get_instruction_text

# Инициализируем FastAPI
app = FastAPI(title="Palliative Care API")


@app.get("/api/hospices")
def read_hospices():
    # Вызываем вашу готовую функцию работы с БД
    df = get_hospices_data()

    if df.empty:
        return []

    # FastAPI не умеет напрямую отдавать DataFrame,
    # поэтому превращаем его в обычный список словарей (JSON)
    return df.to_dict(orient="records")


@app.get("/api/instructions/{instruction_name}")
def read_instruction(instruction_name: str):
    content = get_instruction_text(instruction_name)

    if content is None:
        # Если инструкции нет, возвращаем ошибку 404
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Инструкция не найдена")

    return {"name": instruction_name, "content": content}
