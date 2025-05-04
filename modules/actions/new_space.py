from typing import Any
import datetime
from modules.engine.core import Engine
from modules.actions.continues import continue_last_session

def create_new_space(MainWindow: Any) -> None:
    """
    Создает новое пространство, сохраняет его состояние и загружает последнее сохранение.
    """
    engine = Engine()
    engine.initialize_empty_space()
    print("Новое пространство создано.")

    # Создаем уникальное имя файла с временной меткой
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    save_path = f"cache_space_{timestamp}.json"

    # Сохраняем состояние пространства
    engine.save_space(parent_widget=MainWindow, file_name=save_path)
    print(f"Состояние сохранено в {save_path}.")

    # Загружаем последнее сохранение
    continue_last_session(MainWindow)

# Example usage
if __name__ == "__main__":
    create_new_space()
