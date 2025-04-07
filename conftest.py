import allure
import pytest
import copy

from urls import API_REGISTER, API_LOGIN_OR_DEL
from helper import Helper
from api_client import ApiClient
from data.data import RequestUserData



@allure.step('Вызываем фикстуру создания нового курьера с последующим удалением сущности курьера')
@pytest.fixture(scope='function')
def create_new_user():
    user_data = copy.deepcopy(RequestUserData.payload)

    for key in user_data.keys():
        if key == 'email':
            user_data[key] = Helper.generate_random_string(RequestUserData.LENTH_KEYS_USER) + '@yandex.ru'
            continue
        user_data[key] = Helper.generate_random_string(RequestUserData.LENTH_KEYS_USER)

    response = ApiClient.post(url=API_REGISTER, headers=None, data=user_data)

    yield response

    ApiClient.delete(url=API_LOGIN_OR_DEL, headers={'Authorization': f'{response.json()["accessToken"]}'})
