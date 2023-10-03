import pytest
from hamcrest import assert_that, has_properties
from apis.dm_api_account_grpc.account_pb2 import UserRole


def test_register_account(prepare_user, assertions, orm_db, grpc_account):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password

    grpc_account.create_new_user(
        login=login,
        email=email,
        password=password
    )

    assertions.assert_user_was_created(login=login)
    orm_db.set_activated_flag_by_login(login=login)
    assertions.assert_user_was_activated(login=login)

    response_login = grpc_account.login_as_user(
        login=login,
        password=password,
        remember_me=True
    )
    assert_that(response_login.user.resource, has_properties(
        {
            "login": login,
            "roles": [UserRole.Guest, UserRole.Player]
        }
    ))


@pytest.mark.asyncio
async def test_register_account_async(grpc_account_async, prepare_user, assertions, orm_db):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password

    await grpc_account_async.create_new_user(
        login=login,
        email=email,
        password=password
    )
    assertions.assert_user_was_created(login=login)
    orm_db.set_activated_flag_by_login(login=login)
    assertions.assert_user_was_activated(login=login)

    response_login = await grpc_account_async.login_as_user(
        login=login,
        password=password
    )

    assert_that(response_login.user.resource, has_properties(
        {
            "login": login,
            "roles": [UserRole.Guest, UserRole.Player]
        }
    ))
