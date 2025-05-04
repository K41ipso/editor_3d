import json
import os
from typing import Any
from PyQt5.QtWidgets import QFileDialog
import numpy as np


def save_state(space_data: Any, file_path: str) -> None:
    """
    Сохраняет состояние пространства в файл.
    :param space_data: Данные пространства для сохранения.
    :param file_path: Путь к файлу для сохранения.
    """
    try:
        with open(file_path, 'w') as file:
            json.dump(space_data, file, indent=4)
    except Exception as e:
        print(f"Ошибка при сохранении состояния: {e}")

def load_state(file_path: str = None) -> Any | None:
    """
    Загружает состояние пространства из файла.
    :param file_path: Путь к файлу сохранения.
    :return: Загруженное состояние (NumPy массив) или None, если файл не найден.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл сохранения не найден по пути {file_path}.") # Загружаем данные из файла
        with open(file_path, "r") as file:
            data = json.load(file) # Преобразуем список обратно в NumPy массив
    except Exception as e:
        print(f"Ошибка при загрузке состояния: {e}")
    return data

def load_last_session(saves_directory: str = "saves") -> Any | None:
    """
    Загружает последнее сохранение сессии.
    :param saves_directory: Директория, в которой хранятся файлы сохранений.
    :return: Загруженное состояние (NumPy массив) или None, если сохранения нет.
    """
    try:
        # Получаем список всех файлов в директории сохранений
        files = [os.path.join(saves_directory, f) for f in os.listdir(saves_directory) if f.endswith('.json')]

        # Если файлов нет, возвращаем None
        if not files:
            print("Нет доступных сохранений.")
            return None

        # Находим файл с самой последней датой изменения
        latest_file = max(files, key=os.path.getmtime)

        #выводим логи
        print(f"Продолжение работы в сохранении: {latest_file}")

        # Загружаем состояние из самого свежего файла
        return load_state(latest_file)
    except Exception as e:
        print(f"Ошибка при загрузке последней сессии: {e}")
        return None
