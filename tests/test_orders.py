import allure
import pytest

from copy import deepcopy as dc
from api_client import ApiClient
from data.data import RequestOrderData, ResponseOrderData
from urls import API_ORDERS


@pytest.mark.create_order
@allure.feature('Создание заказа')
class TestCreateOrder:
    @allure.title('Создание заказа с ингредиентами под авторизованным пользователем. Ожидаемый результат: 200')
    def test_create_new_order_with_authorization_and_ingredients_successfully_created(self, create_new_user):
        # Arrange
        token = create_new_user.json()['accessToken']
        payload = RequestOrderData.payload
        # Act
        response = ApiClient.post(url=API_ORDERS, headers={'Authorization': token}, data=payload)
        # Assert
        assert response.status_code == 200 and response.json()['success'] is True
        assert len(response.json()['order']['ingredients']) == len(payload['ingredients'])
        assert response.json()['order']['owner']['email'] == create_new_user.json()['user']['email']

    @allure.title('Создание заказа с ингредиентами без авторизации. Ожидаемый результат: 200')
    def test_create_new_order_without_authorization_and_with_ingredients_successfully_created(self, create_new_user):
        # Arrange
        payload = RequestOrderData.payload
        # Act
        response = ApiClient.post(url=API_ORDERS, data=payload)
        # Assert
        assert response.status_code == 200 and response.json()['success'] is True
        assert isinstance(response.json()['order']['number'], int) and response.json()['order']['number'] > 0

    @allure.title('Создание заказа без ингредиентов. Ожидаемый результат: 400')
    def test_create_order_without_ingredients_failed(self):
        # Arrange
        payload = dc(RequestOrderData.payload)
        payload['ingredients'] = []
        # Act
        response = ApiClient.post(url=API_ORDERS, data=payload)
        # Assert
        assert response.status_code == 400
        assert response.json() == ResponseOrderData.NOT_FOUND_INGREDIENTS_RESPONSE

    @allure.title('Создание заказа с ингредиентом имеющим невалидный хеш. Ожидаемый результат: 500')
    def test_create_order_with_ingredient_that_has_an_invalid_hash_failed(self):
        # Arrange
        incorrect_ingredient_hash = ['61c0c5a71d1f82001bdaaa6c_incorrect']
        payload = dc(RequestOrderData.payload)
        payload['ingredients'] = incorrect_ingredient_hash
        # Act
        response = ApiClient.post(url=API_ORDERS, data=payload)
        # Assert
        assert response.status_code == 500


@pytest.mark.get_order_specific_user
@allure.feature('Получение заказа конкретного пользователя')
class TestGetOrder:
    @allure.title('Получение заказа. Пользователь авторизован. Ожидаемый результат: 200')
    def test_get_order_specific_user_with_authorization_successfully_operation(self, create_new_user):
        # Arrange
        token = create_new_user.json()['accessToken']
        response_create_order = ApiClient.post(url=API_ORDERS, headers={'Authorization': token},
                                               data=RequestOrderData.payload)
        # Act
        response_get_order = ApiClient.get(url=API_ORDERS, headers={'Authorization': token})
        # Assert
        assert response_get_order.status_code == 200
        assert len(response_get_order.json()['orders']) == 1
        assert response_create_order.json()['order']['number'] == response_get_order.json()['orders'][0]['number']

    @allure.title('Получение заказа. Пользователь не авторизован. Ожидаемый результат: 401')
    def test_get_order_without_authorization_failed(self):
        # Act
        response = ApiClient.get(url=API_ORDERS)
        # Assert
        assert response.status_code == 401
        assert response.json() == ResponseOrderData.SHOULD_BE_AUTHORIZED_RESPONSE
