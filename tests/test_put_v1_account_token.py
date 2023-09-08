from hamcrest import assert_that, has_properties, greater_than_or_equal_to
from dm_api_account.models.roles import UserRole
from generic.helpers.data_generator import DataGeneratorHelper
from services.dm_api_account import Facade


def test_put_v1_account_token():
    """
    Test the process of user registration and activation via token.
    """

    # Initialize helper and API client
    data_helper = DataGeneratorHelper()
    api = Facade(host="http://5.63.153.31:5051")

    # Generate data for a new user
    login = data_helper.generate_login()
    password = data_helper.generate_password()
    email = data_helper.generate_email_with_login()

    # Register the new user
    api.account.register_new_user(
        login=login,
        password=password,
        email=email
    )

    # Activate the user using a token from their email
    response = api.account.activate_registered_user(
        login=login
    )

    assert_that(response.resource, has_properties(
        {
            "login": login,
            "roles": [UserRole.GUEST, UserRole.PLAYER],
            "rating": has_properties({
                "enabled": True,
                "quality": greater_than_or_equal_to(0),
                "quantity": greater_than_or_equal_to(0)
            })
        }
    ))
