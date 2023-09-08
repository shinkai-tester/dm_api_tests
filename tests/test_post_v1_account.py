from hamcrest import assert_that, has_properties, has_length
from generic.helpers.data_generator import DataGeneratorHelper
from services.dm_api_account import Facade


def test_post_v1_account():
    """Test the registration and activation of a new user, and assert their initial properties."""

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

    # Assert properties of activated user
    response_activate = api.account.activate_registered_user(login=login)
    assert_that(response_activate.resource, has_properties(
        {
            "login": login,
            "roles": has_length(2),
            "rating": has_properties({
                "enabled": True,
                "quality": 0,
                "quantity": 0
            })
        }
    ))

    # Login the user
    api.login.login_user(
        login=login,
        password=password
    )
