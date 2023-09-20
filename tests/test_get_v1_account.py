from datetime import datetime
from hamcrest import has_properties, assert_that, only_contains, all_of, has_length, greater_than_or_equal_to, \
    has_string, starts_with

from dm_api_account.models.roles import UserRole


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
    dm_api_facade.account.set_headers(headers=token)

    response_user_info = dm_api_facade.account.get_current_user_info()

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
