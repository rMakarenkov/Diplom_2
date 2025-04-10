import allure
import pytest

from copy import deepcopy as dc
from api_client import ApiClient
from data.data import RequestUserData
from helper import Helper
from urls import API_REGISTER, API_LOGIN


@allure.step('Вызываем фикстуру создания нового курьера с последующим удалением сущности курьера')
@pytest.fixture(scope='function')
def create_new_user():
    user_data = dc(RequestUserData.payload)

    for key in user_data.keys():
        if key == 'email':
            user_data[key] = Helper.generate_random_string(RequestUserData.LENTH_KEYS_USER) + '@yandex.ru'
            continue
        user_data[key] = Helper.generate_random_string(RequestUserData.LENTH_KEYS_USER)

    response = ApiClient.post(url=API_REGISTER, data=user_data)

    yield response

    ApiClient.delete(url=API_LOGIN, headers={'Authorization': f'{response.json()["accessToken"]}'})
