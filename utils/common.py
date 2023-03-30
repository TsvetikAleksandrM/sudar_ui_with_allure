import random
from time import sleep, time


def wait(condition, timeout=10, interval=2, err_msg=None):
    """
    Ожидает пока condition не станет True,
    иначе кидает исключение по таймауту
    """
    raise_time = time() + timeout
    while time() < raise_time:
        if condition():
            return
        sleep(interval)
    raise TimeoutError(err_msg)


def rnd_phone():
    """Генерирует рандомный номер телефона"""
    return f'+7{str(random.randint(0, 9999999999)).zfill(10)}'
