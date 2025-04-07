class RequestUserData:
    LENTH_KEYS_USER = 10

    payload = {
        "email": "email_test@yandex.ru",
        "password": "Password",
        "name": "Username"
    }


class ResponseUserData:
    # Create user
    USER_EXISTS_RESPONSE = {
        "success": False,
        "message": "User already exists"
    }

    INCOMPLETE_DATA_RESPONSE = {
        "success": False,
        "message": "Email, password and name are required fields"
    }

    # Login user
    INCORRECT_DATA_RESPONSE = {
        "success": False,
        "message": "email or password are incorrect"
    }

    # Update info user
    NOT_AUTHORIZED_RESPONSE = {
        "success": False,
        "message": "You should be authorised"
    }

    # Delete user
    SUCCESS_DELETE_USER_RESPONSE = {
        "success": True,
        "message": "User successfully removed"
    }


class RequestOrderData:
    payload = {
        "ingredients": ['61c0c5a71d1f82001bdaaa6c', '61c0c5a71d1f82001bdaaa72', '61c0c5a71d1f82001bdaaa70',
                        '61c0c5a71d1f82001bdaaa7a']
    }


class ResponseOrderData:
    NOT_FOUND_INGREDIENTS_RESPONSE = {
        "success": False,
        "message": "Ingredient ids must be provided"
    }
