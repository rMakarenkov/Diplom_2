import json
import allure
import pytest

from api_client import ApiClient
from data.data import ResponseUserData
from urls import API_LOGIN_OR_DEL


@pytest.mark.login_user
@allure.feature('Авторизация пользователя')
class TestLoginUser:
    @allure.title('Авторизация пользователя с корректными данными. Ожидаемый ответ: 200')
    def test_login_user_valid_data_successfully_logged(self, create_new_user):
        # Arrange
        response_create_user = create_new_user
        login_payload = {
            'email': json.loads(response_create_user.request.body)['email'],
            'password': json.loads(response_create_user.request.body)['password']
        }
        # Act
        response_login_user = ApiClient.post(url=API_LOGIN_OR_DEL, headers=None, data=login_payload)
        # Assert
        assert response_login_user.status_code == 200 and response_login_user.json()['success'] == True
        assert response_login_user.json()['user']['email'] == login_payload['email'].lower()

    @allure.title('Авторизация пользователя с неверным логином или паролем. Ожидаемый ответ: 401')
    @pytest.mark.parametrize('key', ['email', 'password'])
    def test_login_user_with_incorrect_email_or_password(self, create_new_user, key):
        # Arrange
        payload = {
            'email': f'{json.loads(create_new_user.request.body)["email"]}',
            'password': f'{json.loads(create_new_user.request.body)["password"]}'
        }
        payload[key] = payload.get(key) + '_'
        # Act
        response = ApiClient.post(url=API_LOGIN_OR_DEL, headers=None, data=payload)
        # Assert
        assert response.status_code == 401
        assert response.json() == ResponseUserData.INCORRECT_DATA_RESPONSE
