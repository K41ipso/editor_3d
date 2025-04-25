from modules.engine.core import Engine


def continue_last_session() -> None:
    """
    Продолжает работу с последним сохранением.
    """
    engine = Engine()
    engine.continue_last_session()
    print("Продолжение работы с последним сохранением.")
