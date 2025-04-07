import json
import allure
import pytest

from api_client import ApiClient
from data.data import ResponseUserData
from urls import API_LOGIN


@pytest.mark.login_user
@allure.feature('Авторизация пользователя')
class TestLoginUser:
    @allure.title('Авторизация пользователя с корректными данными. Ожидаемый результат: 200')
    def test_login_user_valid_data_successfully_login(self, create_new_user):
        # Arrange
        original_payload = json.loads(create_new_user.request.body)
        login_payload = {
            'email': original_payload['email'],
            'password': original_payload['password']
        }
        # Act
        response_login_user = ApiClient.post(url=API_LOGIN, data=login_payload)
        # Assert
        assert response_login_user.status_code == 200
        assert response_login_user.json()['user']['email'] == login_payload['email'].lower()

    @allure.title('Авторизация пользователя с неверным логином или паролем. Ожидаемый результат: 401')
    @pytest.mark.parametrize('key', ['email', 'password'])
    def test_login_user_with_incorrect_email_or_password_failed_login(self, create_new_user, key):
        # Arrange
        original_payload = json.loads(create_new_user.request.body)
        payload = {
            'email': original_payload["email"],
            'password': original_payload["password"]
        }
        payload[key] = payload.get(key) + '_'
        # Act
        response = ApiClient.post(url=API_LOGIN, data=payload)
        # Assert
        assert response.status_code == 401
        assert response.json() == ResponseUserData.INCORRECT_DATA_RESPONSE
