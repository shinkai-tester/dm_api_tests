from datetime import datetime
from hamcrest import has_properties, assert_that, has_length, greater_than_or_equal_to, \
    has_string, starts_with, has_entries


def test_get_v1_account(dm_api_facade, prepare_user, assertions):
    """Test that a user can register, activate, and retrieve their info"""

    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    dm_api_facade.account.register_new_user(
        login=login,
        email=email,
        password=password
    )
    dm_api_facade.account.activate_registered_user(login=login)

    token = dm_api_facade.login.get_auth_token(
        login=login,
        password=password
    )

    response_user_info = dm_api_facade.account.get_current_user_info(x_dm_auth_token=token)

    assert_that(response_user_info.resource, has_entries({
        "login": login,
        "roles": has_length(greater_than_or_equal_to(2)),
        "online": has_string(starts_with(str(datetime.utcnow().date())))
    }))
