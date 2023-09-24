from hamcrest import assert_that, has_properties, greater_than_or_equal_to
from dm_api_account.models.roles import UserRole


def test_put_v1_account_token(dm_api_facade, data_helper, prepare_user, assertions):
    """
    Test the process of user registration and activation via token
    """

    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    dm_api_facade.account.register_new_user(
        login=login,
        password=password,
        email=email
    )

    response = dm_api_facade.account.activate_registered_user(
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
