def test_post_v1_account_login(dm_api_facade, data_helper, prepare_user, assertions):
    """Test the process of registering, activating, and logging in a new user, and assert their initial properties."""

    # Register and activate user
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    dm_api_facade.account.register_new_user(
        login=login,
        email=email,
        password=password
    )
    dm_api_facade.account.activate_registered_user(login=login)

    # Login and assert properties of the user
    response_login = dm_api_facade.login.login_user(
        login=login,
        password=password
    )

    assertions.assert_json_value_by_name(
        response=response_login,
        name="login",
        expected_value=login,
        error_message=f"User login is not equal to {login}",
        path=["resource"]
    )
