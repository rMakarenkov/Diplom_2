import allure
import pytest

from api_client import ApiClient
from data.data import RequestUserData, ResponseUserData
from helper import Helper
from urls import API_UPDATE_USER


@pytest.mark.update_user
@allure.feature('Обновление информации о пользователе')
class TestCreateUser:
    @allure.title('Обновление информации о пользователе с авторизацией. Ожидаемый ответ: 200')
    @pytest.mark.parametrize('key', ['email', 'name'])
    def test_change_user_data_valid_data_with_authorize_successfully_changed(self, create_new_user, key):
        # Arrange
        response_create_user = create_new_user
        token = response_create_user.json()['accessToken']
        payload = {'email': response_create_user.json()['user']['email'],
                   'name': response_create_user.json()['user']['name'],
                   key: Helper.generate_random_string(RequestUserData.LENTH_KEYS_USER) if key == 'name'
                   else Helper.generate_random_string(RequestUserData.LENTH_KEYS_USER).lower() + '@yandex.ru'}
        # Act
        response_update_user = ApiClient.patch(url=API_UPDATE_USER, headers={'Authorization': f'{token}'}, data=payload)
        # Assert
        assert response_update_user.status_code == 200
        assert response_update_user.json()['user'][key] == payload[key]

    @allure.title('Обновление информации о пользователе без авторизации. Ожидаемый ответ: 401')
    def test_change_user_data_valid_data_without_authorize_failed(self, create_new_user):
        # Act
        response_update_user = ApiClient.patch(url=API_UPDATE_USER, headers=None,
                                               data={'email': 'upd' + create_new_user.json()['user']['email'],
                                                     'name': 'upd' + create_new_user.json()['user']['name']})
        # Assert
        assert response_update_user.status_code == 401
        assert response_update_user.json() == ResponseUserData.NOT_AUTHORIZED_RESPONSE
