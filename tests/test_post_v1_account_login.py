from datetime import datetime
from hamcrest import assert_that, has_string, starts_with, has_entries
from dm_api_account.models.roles import UserRole
from generic.helpers.data_generator import DataGeneratorHelper
from services.dm_api_account import Facade


def test_post_v1_account_login():
    """Test the process of registering, activating, and logging in a new user, and assert their initial properties."""

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

    # Login and assert properties of the user
    response_login = api.login.login_user(
        login=login,
        password=password
    ).json()
    assert_that(response_login.get("resource"), has_entries(
        {
            "login": login,
            "roles": [UserRole.GUEST.value, UserRole.PLAYER.value],
            "rating": has_entries({
                "enabled": True,
                "quality": 0,
                "quantity": 0
            }),
            "registration": has_string(starts_with(str(datetime.utcnow().date())))
        }
    ))
