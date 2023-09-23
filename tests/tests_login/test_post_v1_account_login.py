from datetime import datetime
from hamcrest import assert_that, has_entries, has_string, starts_with
from apis.dm_api_account.models.roles import UserRole


def test_post_v1_account_login(dm_api_facade, data_helper, prepare_user, assertions):
    """Test the process of registering, activating, and logging in a new user, and assert their initial properties"""

    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    dm_api_facade.account.register_new_user(
        login=login,
        email=email,
        password=password
    )
    dm_api_facade.account.activate_registered_user(login=login)

    response_login = dm_api_facade.login.login_user(
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
