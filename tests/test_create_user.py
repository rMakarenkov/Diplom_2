import json
import allure
import pytest

from api_client import ApiClient
from data.data import ResponseUserData, RequestUserData
from helper import Helper
from urls import API_REGISTER


@pytest.mark.create_new_user
@allure.feature('Создание пользователя')
class TestCreateUser:
    @allure.title('Создание нового пользователя с корректными данными в request. Ожидаемый результат: 200')
    def test_create_user_valid_data_successfully_created(self, create_new_user):
        # Act
        response = create_new_user
        # Assert
        assert response.status_code == 200
        assert response.json()['user']['email'] == json.loads(response.request.body)['email'].lower()

    @allure.title('Создание дублирующей сущности пользователя. Ожидаемый результат: 403')
    def test_create_user_already_created_failed_created(self, create_new_user):
        # Arrange
        response_new_user = create_new_user
        original_payload = json.loads(response_new_user.request.body)
        # Act
        response_already_exist_user = ApiClient.post(url=API_REGISTER, data=original_payload)
        # Assert
        assert response_already_exist_user.status_code == 403
        assert response_already_exist_user.json() == ResponseUserData.USER_EXISTS_RESPONSE

    @allure.title('Создание пользователя без одного из обязательных ключей в request. Ожидаемый результат: 403')
    @pytest.mark.parametrize('key', ['email', 'name', 'password'])
    def test_create_new_user_required_key_missing_failed_created(self, key):
        # Arrange
        payload = {
            'email': f'{Helper.generate_random_string(RequestUserData.LENTH_KEYS_USER)}@yandex.ru',
            'name': Helper.generate_random_string(RequestUserData.LENTH_KEYS_USER),
            'password': Helper.generate_random_string(RequestUserData.LENTH_KEYS_USER)
        }
        payload.pop(key)
        # Act
        response = ApiClient.post(url=API_REGISTER, data=payload)
        # Assert
        assert response.status_code == 403
        assert response.json() == ResponseUserData.INCOMPLETE_DATA_RESPONSE
