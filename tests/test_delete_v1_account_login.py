from generic.helpers.data_generator import DataGeneratorHelper
from services.dm_api_account import Facade


def test_delete_v1_account_login():
    """Test that a user can successfully log out."""

    # Initialize helper and API client
    data_helper = DataGeneratorHelper()
    api = Facade(host="http://5.63.153.31:5051")

    # Generate user data
    login = data_helper.generate_login()
    password = data_helper.generate_password()
    email = data_helper.generate_email_with_login()

    # Register and activate user
    api.account.register_new_user(
        login=login,
        email=email,
        password=password
    )
    api.account.activate_registered_user(login=login)

    # Authenticate and set token
    token = api.login.get_auth_token(
        login=login,
        password=password
    )
    api.login.set_headers(headers=token)

    # Logout the user
    api.login.logout_user()
