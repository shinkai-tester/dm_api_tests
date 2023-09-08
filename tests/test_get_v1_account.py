from datetime import datetime
from hamcrest import assert_that, has_properties, has_length, greater_than_or_equal_to, all_of, only_contains, \
    has_string, starts_with
from dm_api_account.models.roles import UserRole
from generic.helpers.data_generator import DataGeneratorHelper
from services.dm_api_account import Facade


def test_get_v1_account():
    """Test that a user can register, activate, and retrieve their info."""

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
    api.account.set_headers(headers=token)

    # Retrieve and validate user info
    response_user_info = api.account.get_current_user_info()

    assert_that(response_user_info.resource, has_properties({
        "login": login,
        "roles": all_of(
            only_contains(
                UserRole.GUEST,
                UserRole.PLAYER,
                UserRole.ADMIN,
                UserRole.NANNY_MODERATOR,
                UserRole.REGULAR_MODERATOR,
                UserRole.SENIOR_MODERATOR
            ),
            has_length(greater_than_or_equal_to(2))
        ),
        "online": has_string(starts_with(str(datetime.utcnow().date())))
    }))
