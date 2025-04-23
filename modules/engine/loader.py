import os
import json


def save_state(state, file_path="saves/temp_state.json"):
    """
    Сохраняет состояние пространства в файл.
    :param state: Состояние пространства (например, NumPy массив).
    :param file_path: Путь к файлу сохранения.
    """
    try:
        # Преобразуем NumPy массив в список для сериализации
        if hasattr(state, "tolist"):  # Если это NumPy массив
            state = state.tolist()

        # Создаем директорию, если она не существует
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Сохраняем данные в файл
        with open(file_path, "w") as file:
            json.dump(state, file)
        print(f"Состояние успешно сохранено в {file_path}.")
    except Exception as e:
        print(f"Ошибка при сохранении состояния: {e}")


def load_state(file_path="saves/temp_state.json"):
    """
    Загружает состояние пространства из файла.
    :param file_path: Путь к файлу сохранения.
    :return: Загруженное состояние (NumPy массив) или None, если файл не найден.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл сохранения не найден по пути {file_path}.")

        # Загружаем данные из файла
        with open(file_path, "r") as file:
            data = json.load(file)

        # Преобразуем список обратно в NumPy массив
        import numpy as np
        return np.array(data)
    except Exception as e:
        print(f"Ошибка при загрузке состояния: {e}")
        return None


def load_last_session(default_path="saves/last_session.json"):
    """
    Загружает последнее сохранение сессии.
    :param default_path: Путь к файлу последнего сохранения.
    :return: Загруженное состояние (NumPy массив) или None, если сохранения нет.
    """
    try:
        return load_state(default_path)
    except Exception as e:
        print(f"Ошибка при загрузке последней сессии: {e}")
        return None