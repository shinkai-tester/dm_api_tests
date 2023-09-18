def test_get_v1_account(dm_api_facade, prepare_user, assertions):
    """Test that a user can register, activate, and retrieve their info."""

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

    # Authenticate and set token
    token = dm_api_facade.login.get_auth_token(
        login=login,
        password=password
    )
    dm_api_facade.account.set_headers(headers=token)

    # Retrieve and validate user info
    response_user_info = dm_api_facade.account.get_current_user_info()

    assertions.assert_json_has_keys(
        response=response_user_info,
        names=["login", "roles", "online", "rating", "registration"]
    )
    assertions.assert_json_value_by_name(
        response=response_user_info,
        name="login",
        expected_value=login,
        error_message=f"User login is not equal to {login}",
        path=["resource"]
    )
