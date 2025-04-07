import json
import allure
import pytest

from api_client import ApiClient
from data.data import ResponseUserData
from helper import Helper
from urls import API_REGISTER


@pytest.mark.create_new_user
@allure.feature('Создание пользователя')
class TestCreateUser:
    @allure.title('Создание нового пользователя с корректными данными в request. Ожиаемый ответ: 200')
    def test_create_user_valid_data_successfully_created(self, create_new_user):
        # Act
        response = create_new_user
        # Assert
        assert response.status_code == 200 and response.json()['success'] == True
        assert response.json()['user']['email'] == json.loads(response.request.body)['email'].lower()

    @allure.title('Создание дублирующей сущности пользователя. Ожидаемый ответ: 403')
    def test_create_user_already_created_failed(self, create_new_user):
        # Arrange
        response_new_user = create_new_user
        payload_already_exist_user = {
            'email': json.loads(response_new_user.request.body)['email'],
            'name': json.loads(response_new_user.request.body)['name'],
            'password': json.loads(response_new_user.request.body)['password'],
        }
        # Act
        response_already_exist_user = ApiClient.post(url=API_REGISTER, headers=None, data=payload_already_exist_user)
        # Assert
        assert response_already_exist_user.status_code == 403
        assert response_already_exist_user.json() == ResponseUserData.USER_EXISTS_RESPONSE

    @allure.title('Создание пользователя без одного из обязательных ключей в request. Ожидаемый ответ: 403')
    @pytest.mark.parametrize('key', ['email', 'name', 'password'], ids=lambda x: f'{x} missing')
    def test_create_new_user_required_key_missing_failed(self, key):
        # Arrange
        lenth = 7
        paylaod = {
            'email': f'{Helper.generate_random_string(lenth)} + @yandex.ru',
            'name': Helper.generate_random_string(lenth),
            'password': Helper.generate_random_string(lenth)
        }
        paylaod.pop(key)
        # Act
        response = ApiClient.post(url=API_REGISTER, headers=None, data=paylaod)
        # Assert
        assert response.status_code == 403
        assert response.json() == ResponseUserData.INCOMPLETE_DATA_RESPONSE
