import string
import random
import allure


class Helper:
    @staticmethod
    @allure.step('Вызываем метод генерации рандомной строки. Длина - {lenth}')
    def generate_random_string(lenth: int) -> str:
        charasters = string.digits + string.ascii_letters
        random_string = ''.join(random.choice(charasters) for _ in range(lenth))
        return random_string
