from generic.helpers.data_generator import DataGeneratorHelper
from services.dm_api_account import Facade


def test_put_v1_account_password():
    """Test that a user can successfully reset and change their password."""

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
    auth_token = api.login.get_auth_token(
        login=login,
        password=password
    )
    api.account.set_headers(headers=auth_token)

    # Reset password
    api.account.reset_user_password(
        login=login,
        email=email
    )

    # Generate a new password and change it
    new_password = data_helper.generate_password()
    api.account.change_user_password(
        login=login,
        old_password=password,
        new_password=new_password
    )
