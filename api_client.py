import requests
import allure


class ApiClient:
    @staticmethod
    @allure.step('Вызываем метод GET c параметрами - {params}, эндпоинт - {url}')
    def get(url: str, headers: dict | None, params: dict | None) -> requests.Response:
        return requests.get(url=url, headers=headers, params=params)

    @staticmethod
    @allure.step('Вызываем метод POST c данными - {data}, эндпоинт - {url}')
    def post(url: str, headers: dict | None, data: dict) -> requests.Response:
        return requests.post(url=url, headers=headers, json=data)

    @staticmethod
    @allure.step('Вызываем метод POST c данными - {data}, эндпоинт - {url}')
    def patch(url: str, headers: dict | None, data: dict) -> requests.Response:
        return requests.patch(url=url, headers=headers, json=data)

    @staticmethod
    @allure.step('Вызываем метод DELETE, эндпоинт - {url}')
    def delete(url: str, headers: dict | None,) -> requests.Response:
        return requests.delete(url=url, headers=headers)
