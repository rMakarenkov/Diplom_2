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
    ...


class ResponseOrderData:
    ...
